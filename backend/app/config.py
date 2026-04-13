import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
CALCOM_API_KEY = os.getenv("CALCOM_API_KEY")
CALCOM_EVENT_TYPE_ID = os.getenv("CALCOM_EVENT_TYPE_ID")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
CALCOM_USERNAME = os.getenv("CALCOM_USERNAME", "")

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
