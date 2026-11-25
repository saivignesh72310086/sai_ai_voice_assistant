import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GROK_API_KEY = os.getenv('GROK_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# LLM Config
LLM_PROVIDER = 'grok' if GROK_API_KEY else 'openai' if OPENAI_API_KEY else None
WHISPER_MODEL = os.getenv('WHISPER_MODEL', 'base')

if not LLM_PROVIDER:
    print("⚠️ No API key - using fallback mode")
    LLM_PROVIDER = 'fallback'
else:
    print(f"✅ Using LLM: {LLM_PROVIDER.upper()}")

