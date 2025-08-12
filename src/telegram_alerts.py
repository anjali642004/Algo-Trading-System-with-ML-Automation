import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(text):
    """Send message to Telegram bot"""
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("Telegram credentials not configured")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID, 
        "text": text, 
        "parse_mode": "Markdown"
    }
    
    try:
        r = requests.post(url, data=payload, timeout=10)
        return r.ok
    except Exception as e:
        print(f"Telegram error: {e}")
        return False

def send_signal_alert(ticker, signal, price, rsi, sma20, sma50, date_str):
    """Send formatted trading signal alert"""
    text = f"""{signal} signal for {ticker} on {date_str} at {price:.2f}
RSI={rsi:.2f}, SMA20={sma20:.2f}, SMA50={sma50:.2f}"""
    return send_telegram_message(text)

def send_summary_alert(summary_dict):
    """Send trading summary alert"""
    text = f"""
📊 *Trading Summary Report*

📈 Total Trades: {summary_dict.get('Total Trades', 0)}
✅ Wins: {summary_dict.get('Wins', 0)}
❌ Losses: {summary_dict.get('Losses', 0)}
💰 Net P&L: ₹{summary_dict.get('Net P&L', 0):.2f}
📊 Win Ratio: {summary_dict.get('Win Ratio (%)', 0):.2f}%
"""
    return send_telegram_message(text)

def send_error_alert(error_msg):
    """Send error notification"""
    from datetime import datetime
    text = f"""
⚠️ *System Error Alert*

❌ Error: {error_msg}
🕐 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    return send_telegram_message(text)
