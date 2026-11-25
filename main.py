import speech_recognition as sr
import pyttsx3
import datetime
import sys
from ai_core import sai
from config import *

# --- STEP 1: INITIALIZE THE MOUTH (TEXT-TO-SPEECH) ---
try:
    # 'sapi5' is the standard Windows voice driver
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    # Change [0] to [1] for a female voice
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170) # Speed of speech
except Exception as e:
    print(f"Error initializing voice: {e}")

def speak(text):
    print(f"Sai: {text}")
    engine.say(text)
    engine.runAndWait()

# --- STEP 2: INITIALIZE THE EARS (SPEECH-TO-TEXT) ---
listener = sr.Recognizer()

def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            # Helps Sai filter out your fan or AC noise
            print("Listening... (Speak now)")
            listener.adjust_for_ambient_noise(source, duration=1)
            # Listen for 5 seconds max
            voice = listener.listen(source, timeout=5, phrase_time_limit=8)
            
            print("Processing...")
            command = listener.recognize_google(voice)
            command = command.lower()
            
            # This is the 'Wake Word' filter
            if 'sai' in command:
                command = command.replace('sai', '').strip()
                print(f"You said: {command}")
            else:
                # If you didn't say "Sai", we ignore the command
                return ""
                
    except sr.WaitTimeoutError:
        print("Timeout: No speech detected.")
    except sr.UnknownValueError:
        print("Error: Could not understand audio.")
    except Exception as e:
        print(f"System Error: {e}")
        
    return command

# --- STEP 3: THE BRAIN (LOGIC) ---
echo_mode = False

def run_sai():
    global echo_mode
    command = take_command()
    
    if not command:
        return
    
    if echo_mode:
        speak(command)
        print(f"Sai (Tom): 🗣️ {command}")
        return
    
    if 'tom mode' in command or 'repeat mode' in command:
        if 'on' in command:
            echo_mode = True
            speak("Tom mode activated!")
        else:
            echo_mode = False
            speak("Tom mode off.")
        return
    
    if 'stop' in command or 'exit' in command or 'bye' in command:
        speak("Goodbye!")
        sys.exit()
    
    # AI Response
    try:
        response = sai.chat(command)
        speak(response)
        print(f"Sai: {response}")
    except Exception as e:
        print(f"AI Error: {e}")
        speak("AI not ready. Say 'what time' for basic info.")

# --- STEP 4: START THE ENGINE ---
if __name__ == "__main__":
    # If this fails, your speakers/drivers are the issue
    speak("hi iam sai voice assistant")
    
    while True:
        run_sai()
