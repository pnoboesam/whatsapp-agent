from dotenv import load_dotenv
from pathlib import Path
import os
# from icecream import ic as print

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
# print(OPENROUTER_API_KEY)
