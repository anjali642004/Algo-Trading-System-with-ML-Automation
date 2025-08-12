import pandas as pd
import numpy as np

def sma(series, window):
    """Calculate Simple Moving Average"""
    return series.rolling(window).mean()

def compute_rsi(close, period=14):
    """Calculate Relative Strength Index"""
    delta = close.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_macd(close):
    """Calculate MACD and MACD Signal line"""
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    macd_signal = macd.ewm(span=9, adjust=False).mean()
    return macd, macd_signal

def add_indicators(df):
    """Add all technical indicators to the dataframe"""
    df = df.copy()
    
    # Handle multi-level column names from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        # Get the first level (Price) as column names
        df.columns = df.columns.get_level_values(0)
    
    df['SMA20'] = sma(df['Close'], 20)
    df['SMA50'] = sma(df['Close'], 50)
    df['RSI'] = compute_rsi(df['Close'], 14)
    df['MACD'], df['MACD_SIGNAL'] = compute_macd(df['Close'])
    df['SMA_diff'] = df['SMA20'] - df['SMA50']
    return df
