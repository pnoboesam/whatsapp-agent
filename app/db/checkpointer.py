import os

from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()

DB_URI = os.getenv("DATABASE_URL")

def get_checkpointer():
    return PostgresSaver.from_conn_string(DB_URI)