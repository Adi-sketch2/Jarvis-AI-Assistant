🤖 Jarvis AI Voice Assistant (Python)
📌 Overview

Jarvis is a smart AI-based voice assistant built using Python that can perform various tasks through voice commands. It supports speech recognition, text-to-speech (online & offline), app control, web automation, and AI responses using Gemini API.

🚀 Features
🎤 Voice Command Recognition
🔊 Text-to-Speech (Online via gTTS & Offline via pyttsx3)
🌐 Open Websites (Google, YouTube, Facebook, GitHub, etc.)
💻 Launch Linux Applications (Chrome, VS Code, VLC, etc.)
🎵 Play Songs from Custom Music Library
🔍 YouTube Search for Songs
🧠 AI Responses using Gemini API
🗣 Wake Word Detection ("Jarvis")
🧹 Smart Text Cleaning for Speech Output
⚡ Multi-threaded Speech Execution

🛠️ Technologies Used
Python
SpeechRecognition
pyttsx3 (Offline TTS)
gTTS (Online TTS)
Google Gemini API
Webbrowser Module
Subprocess & OS Modules
dotenv

📂 Project Structure
Jarvis/
│── main.py              # Main assistant logic
│── musiclibrary.py      # Song database
│── .env                 # API keys (not uploaded)
│── README.md            # Project documentation

⚙️ Installation
1️⃣ Clone the Repository
git clone https://github.com/your-username/jarvis-ai.git
cd jarvis-ai

2️⃣ Install Dependencies
pip install -r requirements.txt

(If not using requirements.txt, install manually)

pip install speechrecognition pyttsx3 gtts python-dotenv requests
🔑 Setup Environment Variables

Create a .env file in the root directory:

GEMINI_API_KEY=your_api_key_here
TTS_MODE=online
GTTS_LANG=en
GTTS_SLOW=false
▶️ Run the Project
python main.py
🗣 Example Commands
"Jarvis open Google"
"Jarvis open YouTube"
"Jarvis play Kesariya"
"Jarvis open VS Code"
"Jarvis what is AI?"
🎵 Music Library

The assistant includes a built-in music library with:

Bollywood songs
Old classics
Devotional songs (Radhe Krishna 🙏)

You can add more songs in musiclibrary.py.

⚠️ Requirements
Microphone access
Internet connection (for AI & gTTS)
ffplay installed (for audio playback)
🔮 Future Improvements
GUI Interface (GTK / Tkinter)
Windows & Mac Support
Chat history
More AI integrations
Smart home control
👨‍💻 Author

Aaditya Bhatt
BCA (AI & Data Science) Student

🙏 Acknowledgment

Inspired by real-world AI assistants like Siri, Alexa, and Iron Man’s Jarvis.

💫 Closing

"Your personal AI assistant, always listening, always ready."

Radhe Shyam 🙏

⚡ Bonus (Important)

Before pushing to GitHub:

git init
git add .
git commit -m "Added Jarvis AI Assistant"
git branch -M main
git remote add origin https://github.com/your-username/repo-name.git
git push -u origin main
