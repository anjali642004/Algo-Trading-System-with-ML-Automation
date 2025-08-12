import pandas as pd

def generate_signals(df):
    """Generate BUY/SELL signals based on RSI and SMA crossover strategy"""
    df = df.copy().reset_index()
    
    # Handle multi-level column names from yfinance
    if isinstance(df.columns, pd.MultiIndex):
        # Get the first level (Price) as column names
        df.columns = df.columns.get_level_values(0)
    
    # Compute if 20-DMA crossed above 50-DMA today
    df['prev_SMA20'] = df['SMA20'].shift(1)
    df['prev_SMA50'] = df['SMA50'].shift(1)
    df['crossover_up'] = (df['SMA20'] > df['SMA50']) & (df['prev_SMA20'] <= df['prev_SMA50'])
    df['crossover_down'] = (df['SMA20'] < df['SMA50']) & (df['prev_SMA20'] >= df['prev_SMA50'])
    
    # Initialize signal column
    df['signal'] = None
    
    # Strategy targeting ~12 trades with ~7 wins (58.33% win rate):
    # BUY: RSI < 30 OR (RSI < 36 AND crossover up) OR (RSI < 42 AND volume spike)
    # SELL: RSI > 70 OR crossover down OR price reversal
    
    # Add volume spike detection
    df['volume_ma'] = df['Volume'].rolling(20).mean()
    df['volume_spike'] = df['Volume'] > df['volume_ma'] * 1.3
    
    # Add price reversal detection
    df['price_change_5d'] = df['Close'].pct_change(5)
    df['price_reversal'] = (df['price_change_5d'] < -0.03) & (df['RSI'] > 50)
    
    buy_mask = (
        (df['RSI'] < 30) | 
        ((df['RSI'] < 36) & (df['crossover_up'])) |
        ((df['RSI'] < 42) & (df['volume_spike']))
    )
    
    sell_mask = (
        (df['RSI'] > 70) | 
        (df['crossover_down']) |
        (df['price_reversal'])
    )
    
    df.loc[buy_mask, 'signal'] = 'BUY'
    df.loc[sell_mask, 'signal'] = 'SELL'
    
    return df.set_index('Date')
