import yfinance as yf
import pandas as pd

def fetch_data(ticker, period="1y", interval="1d"):
    """Return df indexed by Date with columns Open, High, Low, Close, Adj Close, Volume"""
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=False)
        df = df.dropna()
        
        # Handle multi-level column names from yfinance
        if isinstance(df.columns, pd.MultiIndex):
            # Get the first level (Price) as column names
            df.columns = df.columns.get_level_values(0)
        
        return df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return pd.DataFrame()
