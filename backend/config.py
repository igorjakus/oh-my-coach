import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

VENDOR_WS_URL = os.getenv("OPENAI_REALTIME_URL")
API_KEY = os.getenv("OPENAI_API_KEY")
