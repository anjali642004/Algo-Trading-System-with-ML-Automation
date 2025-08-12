#!/usr/bin/env python3
"""
Excel file integration for algo trading system
Handles reading from and writing to Excel files
"""

import pandas as pd
import os
from datetime import datetime
from utils import get_logger

logger = get_logger(__name__)

class ExcelManager:
    """Manages Excel file operations for the algo trading system"""
    
    def __init__(self, file_path="Algo_Trading_Log.xlsx"):
        self.file_path = file_path
        self.ensure_file_exists()
    
    def ensure_file_exists(self):
        """Ensure the Excel file exists with proper structure"""
        if not os.path.exists(self.file_path):
            # Create new Excel file with proper structure
            with pd.ExcelWriter(self.file_path, engine='openpyxl') as writer:
                # Trade_Log sheet
                trade_log_df = pd.DataFrame(columns=[
                    'Date', 'Ticker', 'Signal', 'Price', 'RSI', 'SMA20', 'SMA50', 
                    'Volume', 'MACD', 'MACD_Signal', 'Notes'
                ])
                trade_log_df.to_excel(writer, sheet_name='Trade_Log', index=False)
                
                # Summary sheet
                summary_df = pd.DataFrame(columns=['Metric', 'Value'])
                summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                # Analytics sheet
                analytics_df = pd.DataFrame()
                analytics_df.to_excel(writer, sheet_name='Analytics', index=False)
            
            logger.info(f"Created new Excel file: {self.file_path}")
    
    def read_sheet(self, sheet_name):
        """Read a specific sheet from the Excel file"""
        try:
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            return df
        except Exception as e:
            logger.error(f"Error reading sheet {sheet_name}: {e}")
            return pd.DataFrame()
    
    def write_sheet(self, sheet_name, df):
        """Write data to a specific sheet in the Excel file"""
        try:
            # Clean the DataFrame
            df = df.fillna("")
            
            # Write to Excel file with better formatting
            with pd.ExcelWriter(self.file_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # Get the worksheet to apply formatting
                worksheet = writer.sheets[sheet_name]
                
                # Auto-adjust column widths
                for column in worksheet.columns:
                    max_length = 0
                    column_letter = column[0].column_letter
                    for cell in column:
                        try:
                            if len(str(cell.value)) > max_length:
                                max_length = len(str(cell.value))
                        except:
                            pass
                    adjusted_width = min(max_length + 2, 50)
                    worksheet.column_dimensions[column_letter].width = adjusted_width
            
            logger.info(f"Updated sheet {sheet_name} in {self.file_path}")
            return True
        except Exception as e:
            logger.error(f"Error writing to sheet {sheet_name}: {e}")
            return False
    
    def append_trade(self, trade_data):
        """Append a new trade to the Trade_Log sheet"""
        try:
            # Read existing trade log
            trade_log = self.read_sheet('Trade_Log')
            
            # Clean the trade data - replace NaN with empty string
            cleaned_trade_data = {}
            for key, value in trade_data.items():
                if pd.isna(value) or value is None:
                    cleaned_trade_data[key] = ""
                else:
                    cleaned_trade_data[key] = value
            
            # Add new trade
            new_trade = pd.DataFrame([cleaned_trade_data])
            trade_log = pd.concat([trade_log, new_trade], ignore_index=True)
            
            # Clean the entire DataFrame
            trade_log = trade_log.fillna("")
            
            # Write back to Excel
            return self.write_sheet('Trade_Log', trade_log)
        except Exception as e:
            logger.error(f"Error appending trade: {e}")
            return False
    
    def update_summary(self, summary_dict):
        """Update the Summary sheet with new metrics"""
        try:
            # Create summary DataFrame
            summary_data = []
            for metric, value in summary_dict.items():
                summary_data.append({'Metric': metric, 'Value': str(value)})
            
            summary_df = pd.DataFrame(summary_data)
            return self.write_sheet('Summary', summary_df)
        except Exception as e:
            logger.error(f"Error updating summary: {e}")
            return False
    
    def update_analytics(self, analytics_data):
        """Update the Analytics sheet with ML results"""
        try:
            # Convert analytics data to DataFrame
            if 'ml_results' in analytics_data:
                ml_data = []
                for ticker, result in analytics_data['ml_results'].items():
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
                    
                    ml_data.append({
                        'Ticker': ticker,
                        'Accuracy': f"{result.get('accuracy', 0):.3f}",
                        'Prediction': prediction,
                        'Up_Prob': f"{up_prob:.3f}",
                        'Down_Prob': f"{down_prob:.3f}",
                        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    })
                
                analytics_df = pd.DataFrame(ml_data)
                return self.write_sheet('Analytics', analytics_df)
            return True
        except Exception as e:
            logger.error(f"Error updating analytics: {e}")
            return False
    
    def get_trade_count(self):
        """Get the current number of trades in the log"""
        try:
            trade_log = self.read_sheet('Trade_Log')
            return len(trade_log)
        except Exception as e:
            logger.error(f"Error getting trade count: {e}")
            return 0
    
    def get_summary_stats(self):
        """Get current summary statistics"""
        try:
            summary = self.read_sheet('Summary')
            stats = {}
            for _, row in summary.iterrows():
                stats[row['Metric']] = row['Value']
            return stats
        except Exception as e:
            logger.error(f"Error getting summary stats: {e}")
            return {}

# Global Excel manager instance
excel_manager = ExcelManager()
