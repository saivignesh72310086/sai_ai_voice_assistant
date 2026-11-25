import json
import re
from typing import List
import pywhatkit
import wikipedia
import math
from duckduckgo_search import DDGS
import ollama
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import sqlite3
from openai import Whisper  # For STT

# Knowledge base
KNOWLEDGE_FILE
