#gtts
import os
import requests
import speech_recognition as sr
import webbrowser
import musiclibrary
import time
import tempfile
import subprocess
import asyncio
import threading
import json
import difflib
import urllib.parse
from dotenv import load_dotenv
import atexit
import re
import traceback
import pyttsx3
from gtts import gTTS

# Initialize / Globals
recognizer = sr.Recognizer()
FFPLAY_PROCESS = None   # kept for compatibility if you still want ffplay for other audio
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# TTS configuration via env
TTS_MODE = os.getenv("TTS_MODE", "online").lower()   # "online" or "offline"
GTTS_LANG = os.getenv("GTTS_LANG", "en")             # language for gTTS, e.g. "en", "hi"
GTTS_SLOW = os.getenv("GTTS_SLOW", "false").lower()  # "true" or "false"

# Linux apps dict (edit as needed)
LINUX_APPS = {
    "chrome": ["google-chrome"],
    "google chrome": ["google-chrome"],
    "firefox": ["firefox"],
    "vscode": ["code"],
    "code": ["code"],
    "terminal": ["gnome-terminal"],
    "calculator": ["gnome-calculator"],
    "files": ["nautilus"],
    "file manager": ["nautilus"],
    "vlc": ["vlc"],
    "spotify": ["spotify"],
    "whatsapp": ["whatsapp-for-linux"],
}


# Utility: Kill ffplay
def kill_ffplay():
    global FFPLAY_PROCESS
    try:
        if FFPLAY_PROCESS is not None:
            try:
                FFPLAY_PROCESS.kill()
            except Exception:
                pass
            FFPLAY_PROCESS = None
            print("[kill_ffplay] stopped playback")
    except Exception as e:
        print("[kill_ffplay] error:", e)

atexit.register(kill_ffplay)


# Text cleaning for speech (removes markdown and noisy chars)

def clean_for_speech(text: str) -> str:
    if not text:
        return ""
    text = str(text)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\((?:[^)]+)\)", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\((?:[^)]+)\)", r"\1", text)
    text = re.sub(r"(\*\*\*|\*\*|\*|___|__|_)(.*?)\1", r"\2", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*[\-\*\+\•]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"^[\s]*\d+\.\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*{2,}", "", text)
    text = re.sub(r"_\s+", " ", text)
    text = re.sub(r"\s*[_*`~]+\s*", " ", text)
    text = re.sub(r"[\r\n]+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = text.strip()
    text = re.sub(r"\s+[-—–]\s+", ". ", text)
    return text


# OFFLINE pyttsx3 engine and helper
_engine = None

def _get_engine():
    global _engine
    if _engine is None:
        try:
            _engine = pyttsx3.init()
            # Optional: tweak voice properties (rate/volume) here
            try:
                rate = _engine.getProperty('rate')
                _engine.setProperty('rate', int(rate * 0.95))
            except Exception:
                pass
        except Exception as e:
            print('[pyttsx3 init error]:', e)
            traceback.print_exc()
            _engine = None
    return _engine

def _speak_offline(text, block=False):
    """Offline fallback using pyttsx3."""
    text = clean_for_speech(text or "")
    text = text.strip()
    if not text:
        return

    def _run_speech(t):
        try:
            eng = _get_engine()
            if eng is None:
                print('[speak] pyttsx3 engine not available')
                return
            eng.say(t)
            eng.runAndWait()
        except Exception as e:
            print('[speak error pyttsx3]:', e)
            traceback.print_exc()

    if block:
        _run_speech(text)
    else:
        threading.Thread(target=_run_speech, args=(text,), daemon=True).start()


# gTTS (online) helper

def _save_gtts_mp3(text: str, out_path: str, lang: str = "en", slow: bool = False) -> bool:
    try:
        t = gTTS(text=text, lang=lang, slow=slow)
        t.save(out_path)
        return os.path.exists(out_path) and os.path.getsize(out_path) > 200
    except Exception as e:
        print("[gTTS error]:", e)
        traceback.print_exc()
        return False

def _play_mp3(path: str, block=False) -> bool:
    try:
        kill_ffplay()
        proc = subprocess.Popen(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", path],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        if block:
            proc.wait()
            try:
                os.remove(path)
            except Exception:
                pass
        else:
            # schedule removal
            threading.Timer(6, lambda: os.path.exists(path) and os.remove(path)).start()
        return True
    except Exception as e:
        print("[playback error]:", e)
        traceback.print_exc()
        return False


# Unified speak: try online gTTS (if configured), otherwise fallback to offline pyttsx3

def speak(text, block=False, prefer=None):
    text = clean_for_speech(text or "")
    text = text.strip()
    if not text:
        return
    print("Jarvis (speak):", text)

    mode = (prefer or "").lower() or TTS_MODE

    if mode == "online":
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        ok = _save_gtts_mp3(text, tmp, lang=GTTS_LANG, slow=(GTTS_SLOW == "true"))
        if ok and os.path.exists(tmp) and os.path.getsize(tmp) > 200:
            played = _play_mp3(tmp, block=block)
            if played:
                print("[TTS] used gTTS online")
                return
            else:
                print("[TTS] gTTS produced audio but playback failed, falling back")
        else:
            print("[TTS] gTTS failed or produced tiny file, falling back to offline")
            try:
                if os.path.exists(tmp):
                    os.remove(tmp)
            except Exception:
                pass

    # fallback to offline
    _speak_offline(text, block=block)
    print("[TTS] used offline pyttsx3 fallback")


# Gemini API call (left intact)
def call_gemini_api(prompt):
    model = "gemini-2.5-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=payload, timeout=20)
        print(f"[Gemini] Status: {r.status_code}")
        if r.status_code == 200:
            resp = r.json()
            return resp["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print("[Gemini] error:", r.text)
            return "Sorry, Gemini API returned an error. (offline Jarvis can't produce AI answers)"
    except Exception as e:
        print("[Gemini Exception]:", e)
        return "I couldn't connect to Gemini."


# YouTube search fallback

def play_any_song(song_name):
    if not song_name:
        speak("Please tell me which song to play.")
        return
    query = urllib.parse.quote_plus(song_name)
    url = f"https://www.youtube.com/results?search_query={query}"
    speak(f"Searching YouTube for {song_name}")
    webbrowser.open(url)


def shorten_response(text, max_sentences=3):
    if not text:
        return text
    sentences = re.split(r'(?<=[.!?])\s+', text)
    if len(sentences) <= max_sentences:
        return text.strip()
    short_text = " ".join(sentences[:max_sentences])
    return short_text.strip()


# PROCESS COMMAND 

def processCommand(command):
    text = (command or "").lower().strip()
    print("Processing:", text)

    if "open google" in text:
        webbrowser.open("https://google.com")
        speak("Opening Google")
        return

    if "open youtube" in text:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")
        return

    if "open facebook" in text:
        webbrowser.open("https://facebook.com")
        speak("Opening Facebook")
        return

    if "open github" in text:
        webbrowser.open("https://github.com")
        speak("Opening GitHub")
        return

    if "open graphic portal" in text or "open geu" in text:
        webbrowser.open("https://geu.ac.in/")
        speak("Opening the GEU portal")
        return

    # Graphic ERP special handling
    if "graphic erp" in text or "open erp" in text or "erp" in text:
        if "hill" in text:
            webbrowser.open("https://student.gehu.ac.in/")
            speak("Opening Graphic Era Hill student portal")
            return
        if "deemed" in text or "geu" in text or "erp.geu" in text:
            webbrowser.open("https://erp.geu.ac.in/")
            speak("Opening Graphic Era deemed university ERP")
            return
        speak("Deemed or Hill?")
        try:
            with sr.Microphone() as src:
                recognizer.adjust_for_ambient_noise(src, duration=1)
                audio = recognizer.listen(src, timeout=6, phrase_time_limit=3)
            reply = recognizer.recognize_google(audio).lower()
            print("ERP follow-up reply:", reply)
            if "hill" in reply:
                webbrowser.open("https://student.gehu.ac.in/")
                speak("Opening")
                return
            if "deemed" in reply or "geu" in reply:
                webbrowser.open("https://erp.geu.ac.in/")
                speak("Opening")
                return
            speak("I didn't catch that. Opening the student portal by default.")
            webbrowser.open("https://student.gehu.ac.in/")
            return
        except sr.WaitTimeoutError:
            speak("No response. Opening the student portal by default.")
            webbrowser.open("https://student.gehu.ac.in/")
            return
        except Exception as e:
            print("[ERP follow-up error]:", e)
            speak("I couldn't complete that request.")
            return

    if text.startswith("open "):
        app_name = text[len("open "):].strip()
        print("Requested app:", app_name)
        if app_name in LINUX_APPS:
            try:
                subprocess.Popen(LINUX_APPS[app_name])
                speak(f"Opening {app_name}")
            except Exception as e:
                print("[App Error]:", e)
                speak(f"I found {app_name}, but I cannot open it.")
        else:
            print("[App Not Found] available keys:", ", ".join(LINUX_APPS.keys()))
            speak(f"I could not find an installed application named {app_name}.")
        return

    if text.startswith("play"):
        raw_song = text[len("play"):].strip()
        if not raw_song:
            speak("Please tell me which song to play.")
            return

        song = raw_song.lower()
        keys = list(musiclibrary.music.keys())
        lower_keys = [k.lower() for k in keys]

        if song in lower_keys:
            idx = lower_keys.index(song)
            url = musiclibrary.music[keys[idx]]
            speak(f"Playing {keys[idx]}")
            webbrowser.open(url)
            return

        matches = difflib.get_close_matches(song, lower_keys, n=1, cutoff=0.60)
        if matches:
            matched = matches[0]
            idx = lower_keys.index(matched)
            url = musiclibrary.music[keys[idx]]
            speak(f"Playing {keys[idx]}")
            webbrowser.open(url)
            return

        play_any_song(raw_song)
        return

    # DEFAULT: Ask Gemini (may require internet)
    speak("Let me think...")
    answer = call_gemini_api(text)
    answer = clean_for_speech(answer)
    answer = shorten_response(answer)
    speak(answer)


# COMMAND LISTENER

def listen_for_command():
    try:
        print(" Listening for your command...")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.6)
            audio = recognizer.listen(source, timeout=12, phrase_time_limit=5)

        command = recognizer.recognize_google(audio)
        print("Command:", command)
        processCommand(command)

    except sr.UnknownValueError:
        print("Didn't catch that.")
    except sr.WaitTimeoutError:
        print("Timeout waiting for command.")
    except Exception as e:
        print("[Listen Error]:", e)


# WAKE WORD LISTENER

def wake_word_listener():
    while True:
        try:
            print("\nListening for wake word 'Jarvis'...")
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.6)
                audio = recognizer.listen(source, timeout=12, phrase_time_limit=3)

            word = recognizer.recognize_google(audio).lower()
            print("Heard:", word)

            if "jarvis" in word:
                speak("Yes")
                listen_for_command()

        except sr.UnknownValueError:
            continue
        except sr.WaitTimeoutError:
            continue
        except KeyboardInterrupt:
            speak("Goodbye! Radhe Shyam.")
            break
        except Exception as e:
            print("[Wake Listener Error]:", e)


# MAIN

def main():
    speak("Initializing Jarvis.")
    time.sleep(1)
    wake_word_listener()

if __name__ == "__main__":
    main()
