# Sai - Full-Fledged AI Voice Assistant 🚀

Transformed from rule-based to **LLM-powered** (Grok or OpenAI) assistant with tools (YouTube, Wikipedia, calculator, web search), conversation memory.

## Quick Start

1. **Setup .env**:
   ```
   cp .env.example .env
   # Add your key:
   GROK_API_KEY=sk-...
   # or OPENAI_API_KEY=sk-...
   ```

2. **Activate venv** (if not):
   ```
   sai_env\\Scripts\\activate
   pip install -r requirements.txt
   ```

3. **Web Version**:
   ```
   python app.py
   ```
   Open http://localhost:5000 🎤 Click mic or type.

4. **Desktop Version**:
   ```
   python main.py
   ```
   Say "Sai [command]"

## Features
- **Natural conversations** via LLM
- **Voice I/O** (browser STT/TTS web, mic/pyttsx3 desktop)
- **Tools**: Play music, search Wiki/web, math
- **Tom mode**: Echo fun
- **Memory**: Remembers context

## Troubleshooting
- No AI? Check .env keys.
- Voice issues? Install mic drivers.
- Windows TTS slow? Adjust rate in code.

Enjoy your AI Sai! 🎉
