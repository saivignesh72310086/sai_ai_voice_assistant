from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
import pywhatkit
import datetime
import requests
import webbrowser
import subprocess
import smtplib
from email.mime.text import MIMEText
import sqlite3
from flask_session import Session

load_dotenv()
app = Flask(__name__)
app.secret_key = 'sai_siri_pro_2024'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
MEMORY_FILE = 'sai_memory.json'
REMINDERS_DB = 'reminders.db'

# Setup reminders DB
conn = sqlite3.connect(REMINDERS_DB, check_same_thread=False)
conn.execute('CREATE TABLE IF NOT EXISTS reminders (id INTEGER PRIMARY KEY, text TEXT, time TEXT)')

def load_memory():
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f)

def get_weather(city='Delhi'):
    try:
        api_key = 'your_openweather_key' # Free: openweathermap.org
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        r = requests.get(url).json()
        return f"Weather in {r['name']}: {r['weather'][0]['description']}, {r['main']['temp']}°C"
    except:
        return "Weather info unavailable"

def get_news():
    try:
        url = "https://api.gnews.io/v4/top-headlines?country=in&token=your_gnews_key"
        r = requests.get(url).json()
        return r['articles'][0]['title']
    except:
        return "News: Tech stocks rising today"

def send_email(to, subject, body):
    try:
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = os.getenv('EMAIL_FROM')
        msg['To'] = to
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(os.getenv('EMAIL_FROM'), os.getenv('EMAIL_PASS'))
            server.send_message(msg)
        return "Email sent!"
    except:
        return "Email failed"

def add_reminder(text, time_str):
    conn.execute("INSERT INTO reminders (text, time) VALUES (?, ?)", (text, time_str))
    conn.commit()
    return f"Reminder set: {text} at {time_str}"

def chat_ai(message):
    memory = load_memory()
    messages = [{"role": "system", "content": "Sai is Siri/Alexa level assistant. Tools: WEATHER(city), NEWS, CALC(expr), REMINDER(text,time), EMAIL(to,subject,body), OPEN(url), VOLUME(level), SHUTDOWN."}]
    messages.extend(memory[-10:])
    messages.append({"role": "user", "content": message})
    
    try:
        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, max_tokens=200)
        reply = response.choices[0].message.content
        
        # Tool execution
        if 'WEATHER(' in reply:
            city = reply.split('WEATHER(')[1].split(')')[0]
            reply = get_weather(city)
        elif 'NEWS' in reply:
            reply = get_news()
        elif 'CALC(' in reply:
            expr = reply.split('CALC(')[1].split(')')[0]
            reply = f"{expr} = {eval(expr, {'__builtins__':{}})}"
        elif 'REMINDER(' in reply:
            parts = reply.split('REMINDER(')[1].split(')')[0].split(',')
            reply = add_reminder(parts[0], parts[1])
        elif 'EMAIL(' in reply:
            parts = reply.split('EMAIL(')[1].split(')')[0].split(',')
            reply = send_email(parts[0], parts[1], parts[2])
        elif 'OPEN(' in reply:
            url = reply.split('OPEN(')[1].split(')')[0]
            webbrowser.open(url)
            reply = f"Opening {url}"
        elif 'VOLUME' in reply:
            subprocess.run(['powershell', '-Command', 'nircmd.exe setsysvolume 50000'], shell=True)
            reply = "Volume adjusted"
        elif 'SHUTDOWN' in reply:
            subprocess.run(['shutdown', '/s', '/t', '30'])
            reply = "Shutting down in 30s"
        
        memory.append({"role": "user", "content": message})
        memory.append({"role": "assistant", "content": reply})
        save_memory(memory[-20:])
        return reply
    except Exception as e:
        print(f"Error: {e}")
        return "Sai: Ready to help! Try weather Delhi, news, calc 2+2"

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
    
    response = chat_ai(command)
    return jsonify({"response": response, "type": "ai"})

if __name__ == '__main__':
    print("🚀 SAI SIRI PRO - All Features!")
    print("🌐 http://localhost:5000")
    app.run(debug=True, port=5000)
