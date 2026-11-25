from flask import Flask, render_template, request, jsonify, session
from ai_core import sai
from config import *
import pywhatkit
import pyttsx3
import datetime

app = Flask(__name__)
app.secret_key = 'sai_voice_assistant_secret_key_2024'

def process_command(command):
    echo_mode = session.get('echo_mode', False)
    command = command.lower().strip()
    
    if echo_mode:
        return {"response": command, "type": "echo"}
    
    if 'tom mode' in command or 'repeat mode' in command:
        if 'on' in command:
            session['echo_mode'] = True
            session.modified = True
            return {"response": "🐱 Tom mode ON - repeat everything!", "type": "status"}
        else:
            session['echo_mode'] = False
            session.modified = True
            return {"response": "Tom mode OFF - normal AI mode", "type": "status"}
    
    # AI Core Integration
    try:
        response = sai.chat(command)
        return {"response": response, "type": "ai"}
    except Exception as e:
        print(f"AI Error: {e}")
        # Fallback
        if 'time' in command:
            time_str = datetime.datetime.now().strftime('%I:%M %p')
            return {"response": f"The time is {time_str}", "type": "text"}
        elif 'play' in command:
            return {"response": "Playing music (tool active)", "type": "action"}
        return {"response": f"Sai: {sai.chat('hello')}", "type": "text"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/command', methods=['POST'])
def api_command():
    data = request.json
    command = data.get('command', '')
    result = process_command(command)
    return jsonify(result)

if __name__ == '__main__':
    print("🚀 Sai AI Assistant - Tom Mode Fixed!")
    print("🌐 http://localhost:5000")
    print("💡 Add API key to .env for full LLM")
    app.run(debug=True, port=5000)
