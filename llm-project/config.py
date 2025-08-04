import os
from dotenv import load_dotenv

#gemini
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
MODEL = "gemini-2.0-flash-001"

#read content func
MAX_CHARS = 10000
