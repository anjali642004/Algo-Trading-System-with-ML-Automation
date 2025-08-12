from dotenv import load_dotenv
import os

load_dotenv()

TICKERS = [t.strip() for t in os.getenv("TICKERS", "TCS.NS,RELIANCE.NS,INFY.NS").split(",")]
GSHEET_NAME = os.getenv("GSHEET_NAME", "Algo_Trading_Log")
GSPREAD_CREDS = os.getenv("GSPREAD_CREDS", "gsheets_key.json")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
YOUR_EMAIL = os.getenv("YOUR_EMAIL", "your_email@example.com")
