#!/usr/bin/env python3
"""
Test script to verify the algo trading system components
"""

import sys
import os
sys.path.append('src')

def test_imports():
    """Test if all modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from config import TICKERS, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
        print("✅ Config imported successfully")
        print(f"   Tickers: {TICKERS}")
        print(f"   Telegram Token: {TELEGRAM_TOKEN[:10]}...")
        print(f"   Chat ID: {TELEGRAM_CHAT_ID}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from data_fetch import fetch_data
        print("✅ Data fetch imported successfully")
    except Exception as e:
        print(f"❌ Data fetch import failed: {e}")
        return False
    
    try:
        from indicators import add_indicators
        print("✅ Indicators imported successfully")
    except Exception as e:
        print(f"❌ Indicators import failed: {e}")
        return False
    
    try:
        from strategy import generate_signals
        print("✅ Strategy imported successfully")
    except Exception as e:
        print(f"❌ Strategy import failed: {e}")
        return False
    
    try:
        from backtest import backtest_signals
        print("✅ Backtest imported successfully")
    except Exception as e:
        print(f"❌ Backtest import failed: {e}")
        return False
    
    try:
        from ml_model import prepare_features, train_and_eval
        print("✅ ML model imported successfully")
    except Exception as e:
        print(f"❌ ML model import failed: {e}")
        return False
    
    try:
        from sheets import init_sheets
        print("✅ Sheets imported successfully")
    except Exception as e:
        print(f"❌ Sheets import failed: {e}")
        return False
    
    try:
        from telegram_alerts import send_telegram_message
        print("✅ Telegram alerts imported successfully")
    except Exception as e:
        print(f"❌ Telegram alerts import failed: {e}")
        return False
    
    return True

def test_data_fetch():
    """Test data fetching functionality"""
    print("\n📊 Testing data fetch...")
    
    try:
        from data_fetch import fetch_data
        from config import TICKERS
        
        # Test with first ticker
        ticker = TICKERS[0]
        print(f"   Fetching data for {ticker}...")
        
        df = fetch_data(ticker, period="1mo", interval="1d")
        
        if df.empty:
            print(f"❌ No data received for {ticker}")
            return False
        
        print(f"✅ Data fetched successfully for {ticker}")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
        print(f"   Date range: {df.index[0]} to {df.index[-1]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data fetch test failed: {e}")
        return False

def test_indicators():
    """Test technical indicators calculation"""
    print("\n📈 Testing indicators...")
    
    try:
        from data_fetch import fetch_data
        from indicators import add_indicators
        from config import TICKERS
        
        ticker = TICKERS[0]
        df = fetch_data(ticker, period="1mo", interval="1d")
        
        if df.empty:
            print("❌ No data available for indicator test")
            return False
        
        df_with_indicators = add_indicators(df)
        
        required_indicators = ['SMA20', 'SMA50', 'RSI', 'MACD', 'MACD_SIGNAL', 'SMA_diff']
        missing_indicators = [ind for ind in required_indicators if ind not in df_with_indicators.columns]
        
        if missing_indicators:
            print(f"❌ Missing indicators: {missing_indicators}")
            return False
        
        print("✅ All indicators calculated successfully")
        print(f"   Latest RSI: {df_with_indicators['RSI'].iloc[-1]:.2f}")
        print(f"   Latest SMA20: {df_with_indicators['SMA20'].iloc[-1]:.2f}")
        print(f"   Latest SMA50: {df_with_indicators['SMA50'].iloc[-1]:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Indicators test failed: {e}")
        return False

def test_strategy():
    """Test trading strategy signal generation"""
    print("\n🎯 Testing strategy...")
    
    try:
        from data_fetch import fetch_data
        from indicators import add_indicators
        from strategy import generate_signals
        from config import TICKERS
        
        ticker = TICKERS[0]
        df = fetch_data(ticker, period="1mo", interval="1d")
        
        if df.empty:
            print("❌ No data available for strategy test")
            return False
        
        df_with_indicators = add_indicators(df)
        signals_df = generate_signals(df_with_indicators)
        
        if 'signal' not in signals_df.columns:
            print("❌ Signal column not found")
            return False
        
        signals = signals_df['signal'].dropna()
        print(f"✅ Strategy signals generated successfully")
        print(f"   Total signals: {len(signals)}")
        print(f"   Buy signals: {len(signals[signals == 'BUY'])}")
        print(f"   Sell signals: {len(signals[signals == 'SELL'])}")
        
        return True
        
    except Exception as e:
        print(f"❌ Strategy test failed: {e}")
        return False

def test_telegram():
    """Test Telegram integration"""
    print("\n📱 Testing Telegram integration...")
    
    try:
        from telegram_alerts import send_telegram_message
        from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
        
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            print("⚠️ Telegram credentials not configured, skipping test")
            return True
        
        test_message = "🤖 Algo Trading System Test Message\n\nThis is a test message to verify Telegram integration is working correctly."
        
        result = send_telegram_message(test_message)
        
        if result:
            print("✅ Telegram message sent successfully")
        else:
            print("❌ Failed to send Telegram message")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Telegram test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Algo Trading System Tests\n")
    
    tests = [
        ("Imports", test_imports),
        ("Data Fetch", test_data_fetch),
        ("Indicators", test_indicators),
        ("Strategy", test_strategy),
        ("Telegram", test_telegram)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to run.")
        print("\nTo run the system:")
        print("  python src/main.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
