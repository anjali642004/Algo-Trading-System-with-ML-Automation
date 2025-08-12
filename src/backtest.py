from datetime import timedelta
import pandas as pd

def backtest_signals(df, max_hold_days=20):
    """Backtest the trading signals and return performance metrics"""
    trades = []
    position = None
    entry_idx = None
    
    for idx, row in df.iterrows():
        sig = row.get('signal')
        price = row['Close']
        rsi = row['RSI']
        
        if position is None:
            if sig == 'BUY':
                position = {
                    'entry_date': idx, 
                    'entry_price': price, 
                    'entry_rsi': rsi
                }
                entry_idx = idx
        else:
            # Check sell conditions
            days_held = (idx - position['entry_date']).days
            price_change_pct = ((price - position['entry_price']) / position['entry_price']) * 100
            
            # More realistic exit conditions
            if (sig == 'SELL' or 
                rsi > 70 or 
                days_held >= max_hold_days or
                price_change_pct <= -5 or  # Stop loss at 5%
                price_change_pct >= 10):   # Take profit at 10%
                
                exit_price = price
                pnl = exit_price - position['entry_price']
                pnl_pct = (pnl / position['entry_price']) * 100
                
                # Determine exit reason
                if sig == 'SELL':
                    exit_reason = 'SELL_SIGNAL'
                elif rsi > 70:
                    exit_reason = 'RSI_OVERBOUGHT'
                elif price_change_pct <= -5:
                    exit_reason = 'STOP_LOSS'
                elif price_change_pct >= 10:
                    exit_reason = 'TAKE_PROFIT'
                else:
                    exit_reason = 'MAX_DAYS'
                
                trades.append({
                    'entry_date': position['entry_date'],
                    'exit_date': idx,
                    'entry_price': position['entry_price'],
                    'exit_price': exit_price,
                    'pnl': pnl,
                    'pnl_pct': pnl_pct,
                    'days_held': days_held,
                    'exit_reason': exit_reason
                })
                position = None
    
    # Calculate summary statistics
    total = len(trades)
    wins = sum(1 for t in trades if t['pnl'] > 0)
    losses = total - wins
    net_pnl = sum(t['pnl'] for t in trades)
    win_ratio = (wins / total) * 100 if total else 0
    
    return {
        'trades': trades, 
        'total': total, 
        'wins': wins, 
        'losses': losses, 
        'net_pnl': net_pnl, 
        'win_ratio': win_ratio,
        'avg_pnl': net_pnl / total if total else 0,
        'avg_win': sum(t['pnl'] for t in trades if t['pnl'] > 0) / wins if wins else 0,
        'avg_loss': sum(t['pnl'] for t in trades if t['pnl'] < 0) / losses if losses else 0
    }
