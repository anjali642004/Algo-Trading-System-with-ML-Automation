#!/usr/bin/env python3
"""
Setup script for the Algo Trading System
"""

import os
import sys

def create_env_file():
    """Create .env file with user input"""
    print("🔧 Setting up Algo Trading System Configuration\n")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        response = input("⚠️ .env file already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Setup cancelled.")
            return
    
    print("Please provide the following configuration details:\n")
    
    # Stock tickers
    print("📈 Stock Tickers (comma-separated, e.g., TCS.NS,RELIANCE.NS,INFY.NS)")
    tickers = input("Tickers [TCS.NS,RELIANCE.NS,INFY.NS]: ").strip()
    if not tickers:
        tickers = "TCS.NS,RELIANCE.NS,INFY.NS"
    
    # Google Sheets
    print("\n📋 Google Sheets Configuration")
    gsheet_name = input("Sheet name [Algo_Trading_Log]: ").strip()
    if not gsheet_name:
        gsheet_name = "Algo_Trading_Log"
    
    gspread_creds = input("Service account JSON file [gsheets_key.json]: ").strip()
    if not gspread_creds:
        gspread_creds = "gsheets_key.json"
    
    # Telegram
    print("\n📱 Telegram Bot Configuration")
    print("To get your bot token:")
    print("1. Message @BotFather on Telegram")
    print("2. Send /newbot and follow instructions")
    print("3. Copy the token provided")
    
    telegram_token = input("Bot token: ").strip()
    
    print("\nTo get your chat ID:")
    print("1. Send a message to your bot")
    print("2. Visit: https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates")
    print("3. Find 'chat':{'id': <number>} in the response")
    
    telegram_chat_id = input("Chat ID: ").strip()
    
    # Email
    print("\n📧 Email Configuration")
    email = input("Your email (for Google Sheets access): ").strip()
    
    # Create .env file
    env_content = f"""# Algo Trading System Configuration
TICKERS={tickers}
GSHEET_NAME={gsheet_name}
GSPREAD_CREDS={gspread_creds}
TELEGRAM_TOKEN={telegram_token}
TELEGRAM_CHAT_ID={telegram_chat_id}
YOUR_EMAIL={email}
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("\n✅ .env file created successfully!")
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}")
        return
    
    print("\n📋 Next Steps:")
    print("1. Ensure gsheets_key.json is in the project root")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Test the system: python test_system.py")
    print("4. Run the system: python src/main.py")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'pandas', 'numpy', 'yfinance', 'gspread', 
        'google-auth', 'python-dotenv', 'scikit-learn', 
        'requests', 'schedule'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies are installed!")
        return True

def check_files():
    """Check if required files exist"""
    print("\n📁 Checking required files...")
    
    required_files = [
        'gsheets_key.json',
        'requirements.txt',
        'src/config.py',
        'src/main.py'
    ]
    
    missing_files = []
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {', '.join(missing_files)}")
        if 'gsheets_key.json' in missing_files:
            print("Download gsheets_key.json from Google Cloud Console")
        return False
    else:
        print("\n✅ All required files are present!")
        return True

def main():
    """Main setup function"""
    print("🚀 Algo Trading System Setup\n")
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check files
    files_ok = check_files()
    
    if not deps_ok or not files_ok:
        print("\n⚠️ Please fix the issues above before continuing.")
        return
    
    # Create .env file
    create_env_file()

if __name__ == "__main__":
    main()
