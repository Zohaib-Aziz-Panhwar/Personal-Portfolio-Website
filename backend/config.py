"""
Configuration settings for the FastAPI application.
Loads environment variables from .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Application settings
APP_NAME = os.getenv("APP_NAME", "Portfolio API")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Server settings
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8000"))

# MongoDB settings (check both MONGODB_URL and MONGO_URI for compatibility)
MONGODB_URL = os.getenv("MONGODB_URL") or os.getenv("MONGO_URI", "")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "portfolio_db")
MONGODB_COLLECTION_NAME = os.getenv("MONGODB_COLLECTION_NAME", "contacts")

# Email settings
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")  # Your email address
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")  # Your email password or app password
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "panwerzohaib2@gmail.com")  # Email where you want to receive notifications

