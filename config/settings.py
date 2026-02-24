import os
from dotenv import load_dotenv

load_dotenv()

IRMS_BASE_URL = os.getenv("IRMS_BASE_URL")
IRMS_EMAIL = os.getenv("IRMS_EMAIL")
IRMS_PASSWORD = os.getenv("IRMS_PASSWORD")
HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
