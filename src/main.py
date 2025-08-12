import time
import pandas as pd
from datetime import datetime

from config import TICKERS
from data_fetch import fetch_data
from indicators import add_indicators
from strategy import generate_signals
from backtest import backtest_signals
from ml_model import prepare_features, train_and_eval, predict_next_day
from sheets import init_sheets, append_trade, update_summary, update_analytics
from excel_integration import excel_manager
from telegram_alerts import send_signal_alert, send_summary_alert, send_error_alert
from utils import get_logger, format_currency, format_percentage, validate_data

logger = get_logger("mini-algo")

def run_once():
    """Run one complete scan of all tickers"""
    logger.info(f"Starting scan for: {', '.join(TICKERS)}")
    
    try:
        # Initialize Google Sheets
        sheets = init_sheets()
        trade_ws = sheets['trade']
        summary_ws = sheets['summary']
        analytics_ws = sheets['analytics']
        
        overall_summary = {
            'Total Trades': 0, 
            'Wins': 0, 
            'Losses': 0, 
            'Net P&L': 0,
            'Total Tickers': len(TICKERS),
            'Scan Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        ml_results = {}
        
        for ticker in TICKERS:
            # Fetch data
            df = fetch_data(ticker, period="6mo", interval="1d")
            
            # Validate data
            is_valid, validation_msg = validate_data(df, ticker)
            if not is_valid:
                logger.warning(f"⚠️ {validation_msg}")
                continue
            
            # Add technical indicators
            df = add_indicators(df)
            
            # Generate signals
            signals_df = generate_signals(df)
            
            # Find recent signals (last 5 days)
            recent_signals = signals_df.dropna(subset=['signal']).tail(5)
            
            # Log recent signals to Google Sheets and send Telegram alerts
            for idx, row in recent_signals.iterrows():
                if row['signal'] in ['BUY', 'SELL']:
                    date_str = idx.strftime("%Y-%m-%d")
                    price = row['Close']
                    rsi = row['RSI']
                    sma20 = row['SMA20']
                    sma50 = row['SMA50']
                    volume = row['Volume']
                    macd = row['MACD']
                    macd_signal = row['MACD_SIGNAL']
                    
                    # Prepare row data for Google Sheets
                    row_data = [
                        date_str, ticker, row['signal'], float(price), 
                        float(rsi), float(sma20), float(sma50), 
                        float(volume), float(macd), float(macd_signal), ""
                    ]
                    
                    # Append to Google Sheets
                    append_trade(trade_ws, row_data)
                    
                    # Also append to Excel file
                    excel_trade_data = {
                        'Date': date_str,
                        'Ticker': ticker,
                        'Signal': row['signal'],
                        'Price': float(price),
                        'RSI': float(rsi),
                        'SMA20': float(sma20),
                        'SMA50': float(sma50),
                        'Volume': float(volume),
                        'MACD': float(macd),
                        'MACD_Signal': float(macd_signal),
                        'Notes': ""
                    }
                    excel_success = excel_manager.append_trade(excel_trade_data)
                    
                    # Send Telegram alert
                    telegram_sent = send_signal_alert(ticker, row['signal'], price, rsi, sma20, sma50, date_str)
                    
                    # Log in exact format requested
                    logger.info(f"Found {row['signal']} for {ticker} on {date_str} @ {price:.2f} (RSI={rsi:.2f}, SMA20={sma20:.2f}, SMA50={sma50:.2f}) -> logged to Google Sheets & Excel")
                    logger.info(f"Telegram sent: {telegram_sent}")
            
            # Run backtest
            bt_results = backtest_signals(signals_df)
            
            # Update overall summary
            overall_summary['Total Trades'] += bt_results['total']
            overall_summary['Wins'] += bt_results['wins']
            overall_summary['Losses'] += bt_results['losses']
            overall_summary['Net P&L'] += bt_results['net_pnl']
            
            # Log backtest results in exact format
            logger.info(f"Backtest {ticker} | Trades={bt_results['total']} | Wins={bt_results['wins']} | Net P&L={bt_results['net_pnl']:.2f} | WinRatio={bt_results['win_ratio']:.2f}%")
            
            # Train ML model
            features, target = prepare_features(df)
            if len(features) > 50:
                ml_result = train_and_eval(features, target)
                ml_results[ticker] = ml_result
                
                # Make prediction for next day
                if ml_result['model'] is not None:
                    prediction = predict_next_day(ml_result['model'], df)
                    ml_result['prediction'] = prediction
                
                # Log ML results in exact format
                logger.info(f"{ticker} ML acc: {ml_result['accuracy']:.3f}")
        
        # Calculate final metrics
        total_trades = overall_summary['Total Trades']
        if total_trades > 0:
            overall_summary['Win Ratio (%)'] = round((overall_summary['Wins'] / total_trades) * 100, 2)
            overall_summary['Avg P&L per Trade'] = round(overall_summary['Net P&L'] / total_trades, 2)
        else:
            overall_summary['Win Ratio (%)'] = 0
            overall_summary['Avg P&L per Trade'] = 0
        
        # Update Google Sheets
        update_summary(summary_ws, overall_summary)
        update_analytics(analytics_ws, {'ml_results': ml_results})
        
        # Also update Excel file
        excel_manager.update_summary(overall_summary)
        excel_manager.update_analytics({'ml_results': ml_results})
        
        # Send summary to Telegram
        send_summary_alert(overall_summary)
        
        logger.info("Scan complete.")
        
    except Exception as e:
        error_msg = f"Error in algo trading scan: {str(e)}"
        logger.error(error_msg)
        send_error_alert(error_msg)

def run_scheduled():
    """Run the system on a schedule"""
    import schedule
    
    # Schedule to run every day at 9:30 AM (market open)
    schedule.every().day.at("09:30").do(run_once)
    
    # Also run once immediately
    run_once()
    
    logger.info("🕐 Scheduling daily runs at 9:30 AM...")
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--scheduled":
        run_scheduled()
    else:
        run_once()
