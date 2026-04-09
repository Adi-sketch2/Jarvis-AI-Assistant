# 🤖 Jarvis AI Voice Assistant  

---

## 📌 Overview  

This project is a **Python-based AI Voice Assistant** inspired by Jarvis (Iron Man).  
It listens to voice commands, processes them intelligently, and performs tasks like opening apps, playing music, browsing the web, and answering questions using AI.

It combines **Speech Recognition, Text-to-Speech, and AI integration** to create a real-time smart assistant.

---

## 🚀 Features  

- 🎤 Voice command recognition  
- 🗣 Wake word detection ("Jarvis")  
- 🔊 Text-to-Speech (Online + Offline)  
- 🌐 Open websites (Google, YouTube, GitHub, etc.)  
- 💻 Launch Linux applications  
- 🎵 Play songs from custom music library  
- 🔍 Automatic YouTube search for songs  
- 🧠 AI responses using Gemini API  
- ⚡ Multi-threaded execution  
- 🧹 Clean speech output processing  

---

## 🧠 System Approach  

- **Type:** AI Voice Assistant  
- **Flow:**  
  - Wake word detection  
  - Speech recognition  
  - Command processing  
  - Action execution / AI response  
  - Voice output  

---

## 📊 Modules  

### 🎙 Input Module  
- Captures voice via microphone  
- Converts speech → text  

### ⚙️ Processing Module  
- Matches predefined commands  
- Uses AI for unknown queries  

### 🔊 Output Module  
- Converts text → speech  
- Uses:
  - gTTS (Online)  
  - pyttsx3 (Offline)  

---

## 🎵 Music System  

- Uses `musiclibrary.py`  
- Includes:
  - Bollywood songs  
  - Old classics  
  - Devotional songs  
- If song not found → searches YouTube automatically  

---

## 🛠️ Technologies Used  

- **Language:** Python  
- **Libraries:**  
  - SpeechRecognition  
  - pyttsx3  
  - gTTS  
  - requests  
  - python-dotenv  
- **Tools:** ffplay, subprocess  
- **API:** Gemini API  

---

## 📁 Project Structure  

```bash
Jarvis/
│── main.py
│── musiclibrary.py
│── .env
│── README.md
```

---

## ⚙️ Setup  

### 1. Clone Repository  

```bash
git clone https://github.com/your-username/jarvis-ai.git
cd jarvis-ai
```

---

### 2. Install Dependencies  

```bash
pip install speechrecognition pyttsx3 gtts python-dotenv requests
```

---

### 3. Create `.env` File  

```
GEMINI_API_KEY=your_api_key_here
TTS_MODE=online
GTTS_LANG=en
GTTS_SLOW=false
```

---

## ▶️ Run  

```bash
python main.py
```

---

## 🎤 Example Commands  

- Jarvis open Google  
- Jarvis play Kesariya  
- Jarvis open YouTube  
- Jarvis open VS Code  
- Jarvis what is AI  

---

## ⚠️ Requirements  

- Microphone  
- Internet connection  
- ffplay installed  

---

## 🔮 Future Improvements  

- GUI Interface  
- Cross-platform support  
- Chat memory  
- Smart home integration  

---

## 👨‍💻 Author  

**Aaditya Bhatt**  


---

## 🌟 Support  

If you like this project, give it a ⭐ on GitHub!  

---

## 💫 Conclusion  

This project demonstrates how **AI + Voice Processing + Automation** can be combined to build a real-world assistant.