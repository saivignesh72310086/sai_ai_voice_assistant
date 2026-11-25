from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import pywhatkit
import datetime
from flask_session import Session

load_dotenv()
app = Flask(__name__)
app.secret_key = 'sai_pro_2024_secret'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
MEMORY_FILE = 'sai_memory.json'

def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

def chat_ai(message):
    memory = load_memory()
    messages = [{"role": "system", "content": "You are Sai, like Siri/Alexa. Concise, helpful, fun. Use tools when needed."}]
    messages.extend(memory[-10:])
    messages.append({"role": "user", "content": message})
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150
        )
        reply = response.choices[0].message.content
        memory.append({"role": "user", "content": message})
        memory.append({"role": "assistant", "content": reply})
        save_memory(memory[-20:])  # Keep last 20
        return reply
    except Exception as e:
        print(f"AI Error: {e}")
        return "Sai here! Tell me what you need."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def api_chat():
    data = request.json
    command = data.get('command', '')
    session['echo_mode'] = data.get('echo_mode', False)
    
    if session.get('echo_mode'):
        return jsonify({"response": command, "type": "echo"})
    
    if 'tom mode' in command:
        session['echo_mode'] = 'on' in command
        return jsonify({"response": f"Tom mode {'ON' if session['echo_mode'] else 'OFF'}!", "type": "status"})
    
    response = chat_ai(command)
    return jsonify({"response": response, "type": "ai"})

if __name__ == '__main__':
    print("🚀 SAI PRO - Siri/Alexa Level")
    print("🌐 http://localhost:5000")
    app.run(debug=True, port=5000)
