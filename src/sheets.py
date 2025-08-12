import gspread
from gspread.exceptions import SpreadsheetNotFound
from config import GSHEET_NAME, GSPREAD_CREDS, YOUR_EMAIL

def init_sheets():
    """Initialize Google Sheets connection and create required worksheets"""
    gc = gspread.service_account(filename=GSPREAD_CREDS)
    
    try:
        sh = gc.open(GSHEET_NAME)
    except SpreadsheetNotFound:
        sh = gc.create(GSHEET_NAME)
        # Share with your personal email so you can see it in your Drive
        if YOUR_EMAIL:
            sh.share(YOUR_EMAIL, role='writer', type='user')
    
    # Ensure worksheets exist
    def ensure_ws(title):
        try:
            return sh.worksheet(title)
        except:
            return sh.add_worksheet(title=title, rows="1000", cols="20")
    
    trade_ws = ensure_ws("Trade_Log")
    summary_ws = ensure_ws("Summary")
    analytics_ws = ensure_ws("Analytics")
    
    # Set up headers for trade log
    trade_headers = [
        "Date", "Ticker", "Signal", "Price", "RSI", "SMA20", "SMA50", 
        "Volume", "MACD", "MACD_Signal", "Notes"
    ]
    trade_ws.update('A1:K1', [trade_headers])
    
    return {
        'sh': sh, 
        'trade': trade_ws, 
        'summary': summary_ws, 
        'analytics': analytics_ws
    }

def append_trade(ws_trade, row):
    """Append a trade signal to the trade log"""
    ws_trade.append_row(row)

def update_summary(ws_summary, summary_dict):
    """Update the summary worksheet with performance metrics"""
    ws_summary.clear()
    rows = [["Metric", "Value"]]
    for k, v in summary_dict.items():
        rows.append([k, str(v)])
    ws_summary.update(rows)

def update_analytics(ws_analytics, analytics_data):
    """Update the analytics worksheet with ML model results"""
    ws_analytics.clear()
    
    if 'ml_results' in analytics_data:
        ml_data = analytics_data['ml_results']
        rows = [["Ticker", "Accuracy", "Prediction", "Up_Prob", "Down_Prob"]]
        
        for ticker, result in ml_data.items():
            if result['model'] is not None:
                # Extract prediction data safely
                prediction_data = result.get('prediction', {})
                if isinstance(prediction_data, dict):
                    prediction = prediction_data.get("prediction", "N/A")
                    up_prob = prediction_data.get("up_probability", 0)
                    down_prob = prediction_data.get("down_probability", 0)
                else:
                    prediction = "N/A"
                    up_prob = 0
                    down_prob = 0
                
                # Append clean row to Analytics sheet
                rows.append([
                    ticker,
                    round(result['accuracy'], 3),
                    prediction,
                    round(up_prob, 3),
                    round(down_prob, 3)
                ])
        
        ws_analytics.update(rows)
