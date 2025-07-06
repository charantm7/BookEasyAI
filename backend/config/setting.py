import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_CREDENTIAL_PATH = os.getenv("GOOGLE_CREDENTIAL_PATH")

GOOGLE_CALENDAR_ID = os.getenv("GOOGLE_CALENDAR_ID")