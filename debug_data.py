#!/usr/bin/env python3
"""
Debug script to understand yfinance data structure
"""

import yfinance as yf
import pandas as pd

def debug_data():
    """Debug the data structure from yfinance"""
    ticker = "TCS.NS"
    print(f"Fetching data for {ticker}...")
    
    df = yf.download(ticker, period="1mo", interval="1d", progress=False, auto_adjust=False)
    
    print(f"DataFrame shape: {df.shape}")
    print(f"DataFrame columns: {df.columns}")
    print(f"Column type: {type(df.columns)}")
    print(f"Is MultiIndex: {isinstance(df.columns, pd.MultiIndex)}")
    
    if isinstance(df.columns, pd.MultiIndex):
        print("MultiIndex columns:")
        for i, col in enumerate(df.columns):
            print(f"  {i}: {col}")
        
        # Flatten column names
        flattened_columns = [col[1] if col[1] else col[0] for col in df.columns]
        print(f"Flattened columns: {flattened_columns}")
        
        # Create new dataframe with flattened columns
        df_flat = df.copy()
        df_flat.columns = flattened_columns
        print(f"Flattened DataFrame columns: {df_flat.columns}")
        print(f"Sample data:")
        print(df_flat.head())
    else:
        print("Regular columns:")
        print(df.head())

if __name__ == "__main__":
    debug_data()
