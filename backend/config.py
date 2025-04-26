import os

from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

# Database configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "hackathon")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "hackathon")
POSTGRES_DB = os.getenv("POSTGRES_DB", "hackathon")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
