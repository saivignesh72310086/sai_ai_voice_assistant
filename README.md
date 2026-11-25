# sai_ai_voice_assistant
A voice-controlled AI assistant similar to Siri and Alexa, capable of:

Listening to voice commands
Playing songs and videos
Opening applications
Answering questions with AI knowledge
🚀 Quick Start
Web Interface (Recommended)
Option 1: Double-click the batch file

run_web.bat
Option 2: Command line

streamlit run web_sai.py
Option 3: Full Python path

C:/Users/Lenovo 6NIN/AppData/Local/Programs/Python/Python312/python.exe -m streamlit run web_sai.py
Then open your browser to: http://localhost:8501

Command Line Version
python sai_assistant.py
Test Scripts
python test_sai.py          # Test basic functionality
python test_social.py       # Test social media features
Setup
Install required packages (already done):

openai
speechrecognition
pyttsx3
pygame
pyaudio
streamlit
Ensure you have a microphone for voice input.

For media playback, update the file paths in media_player.py and command_parser.py with actual song/video files.

Note: The provided OpenAI API key has exceeded its quota. To enable full AI responses, add credits to your OpenAI account or use a different API key.

Usage
Web Interface Features:
Voice Commands: Click "Start Listening" and speak
Text Commands: Type in the text box
Quick Commands: Pre-made buttons for common tasks
Command History: See your conversation history
Voice Commands:
"What is the weather today?"
"Open WhatsApp" - Opens WhatsApp Web
"Open Instagram" - Opens Instagram
"Open Facebook" - Opens Facebook
"Search for [topic]" - Searches the web for a topic
"Search Instagram for [topic]" - Searches Instagram for a topic
"Search Facebook for [topic]" - Searches Facebook for a topic
"Play [song name]" - Searches YouTube and plays the first matching video
"Learn [subject]" - Opens a YouTube lecture video for the subject
"2+2" / "Add 2 and 3" / "Multiply 4 by 5" / "Square 7" / "Cube 3" / "Square root of 16" - Performs math operations
"Open notepad" - Opens Windows Notepad
"Play a song" - Media playback (requires configuration)
"Play video" - Video playback (requires configuration)
"Stop" - Stops media playback
"Exit" to quit
Features
Voice Recognition: Uses Google Speech Recognition
AI Responses: Powered by OpenAI GPT-3.5 (currently using mock responses due to quota limits)
Text-to-Speech: Uses pyttsx3 (command line) / Web Speech API (web)
Media Playback: Basic song/video playing with pygame
App Launching: Opens common Windows apps
Social Media Integration: Open WhatsApp, Instagram, Facebook and search topics
Web Interface: Modern, responsive web UI with Streamlit
Security Note
The API key is stored in config.py. In production, consider using environment variables for security.

Current Limitations
OpenAI API quota exceeded - using mock responses
Media files need to be specified with actual paths
App launching limited to basic Windows apps
Voice recognition in web version requires microphone permissions
