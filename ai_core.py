import json
from typing import List, Dict
from config import LLM_PROVIDER, GROK_API_KEY, OPENAI_API_KEY
from openai import OpenAI
import pywhatkit
import wikipedia
import math
from duckduckgo_search import DDGS

# Conversation memory
memory = []

class SaiAI:
    def __init__(self):
        self.client = self._init_client()
        self.tools = {
            'youtube': self._play_youtube,
            'wikipedia': self._wikipedia_search,
            'calculator': self._calculator,
            'web_search': self._web_search
        }
    
    def _init_client(self):
        if LLM_PROVIDER == 'grok' and GROK_API_KEY:
            try:
                from grok import Grok
                return Grok(api_key=GROK_API_KEY)
            except:
                print("Grok not available, using OpenAI")
        if LLM_PROVIDER == 'openai' and OPENAI_API_KEY:
            return OpenAI(api_key=OPENAI_API_KEY)
        print("No LLM - using smart fallback")
        return None
    
    def chat(self, user_input: str) -> str:
        memory.append({'role': 'user', 'content': user_input})
        messages = [{'role': 'system', 'content': 'You are Sai, helpful voice assistant. Concise answers.'}]
        messages.extend(memory[-6:])
        
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model='gpt-4o-mini' if LLM_PROVIDER == 'openai' else 'grok-beta',
                    messages=messages,
                    max_tokens=150
                )
                content = response.choices[0].message.content
                memory.append({'role': 'assistant', 'content': content})
                return content
            except Exception as e:
                print(f"LLM error: {e}")
        
        # Smart fallback
        user_input_lower = user_input.lower()
        if 'time' in user_input_lower:
            from datetime import datetime
            return f"Current time: {datetime.now().strftime('%I:%M %p')}"
        elif 'play' in user_input_lower:
            return "Playing music on YouTube..."
        return "Try 'time', 'play song', 'tom mode on'"
    
    def _play_youtube(self, query):
        pywhatkit.playonyt(query)
        return f"Playing {query}"
    
    def _wikipedia_search(self, query):
        try:
            return wikipedia.summary(query, 1)
        except:
            return "Info not found"
    
    def _calculator(self, expr):
        try:
            result = eval(expr, {"__builtins__": {}, "math": math})
            return str(result)
        except:
            return "Math error"
    
    def _web_search(self, query):
        try:
            with DDGS() as ddgs:
                r = next(ddgs.text(query))
            return r['body'][:200]
        except:
            return "Search failed"

sai = SaiAI()

