import logging
import pandas as pd
from datetime import datetime

def get_logger(name=__name__):
    """Set up logging configuration"""
    logging.basicConfig(
        format="%(asctime)s %(levelname)s: %(message)s",
        level=logging.INFO,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('algo_trading.log', encoding='utf-8')
        ]
    )
    return logging.getLogger(name)

def format_currency(amount):
    """Format amount as Indian Rupees"""
    return f"₹{amount:,.2f}"

def format_percentage(value):
    """Format value as percentage"""
    return f"{value:.2f}%"

def get_current_time():
    """Get current timestamp"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate_data(df, ticker):
    """Validate data quality"""
    if df.empty:
        return False, f"No data available for {ticker}"
    
    # Handle multi-level column names from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        # Get the first level (Price) as column names
        df.columns = df.columns.get_level_values(0)
    
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        return False, f"Missing columns for {ticker}: {missing_columns}"
    
    if len(df) < 50:
        return False, f"Insufficient data for {ticker}: {len(df)} rows"
    
    return True, "Data validation passed"
