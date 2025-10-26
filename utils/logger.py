from datetime import datetime
import json
import os

from robinhood.client import CryptoAPITrading


class Logger:
    def __init__(self, log_dir="logs"):
        # Create logs directory if it doesn't exist
        os.makedirs(log_dir, exist_ok=True)
        
        # Generate filename with current datetime
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_file = os.path.join(log_dir, f"{timestamp}.log")
        
        # Initialize the Robinhood client
        self.client = CryptoAPITrading()
    
    def log(self, message=None):
        timestamp = datetime.now().isoformat()
        
        # Get current holdings
        holdings = self.client.get_holdings()
        
        # Create log entry with holdings and optional message
        log_entry = {
            "timestamp": timestamp,
            "holdings": holdings
        }
        
        if message:
            log_entry["message"] = message
        
        with open(self.log_file, "a") as f:
            f.write(json.dumps(log_entry, indent=2) + os.linesep)