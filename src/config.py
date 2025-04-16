"""Configuration file for Binance Trading Bot"""

import os

from dotenv_vault import load_dotenv

_ = load_dotenv()

# Application configuration
APP_NAME = "expert"  # Expert name for the bot

# Logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL")  # Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
LOG_NAME = APP_NAME  # Logger name
LOG_FORMAT = os.getenv("LOG_FORMAT")  # Log format
LOG_CONFIG = os.getenv("LOG_CONFIG")  # Log configuration file name
LOG_FILE = os.getenv("LOG_FILE")  # Log file name
LOG_MAX_SIZE = os.getenv("LOG_MAX_SIZE")  # Maximum log file size (10 * 1024 * 1024 = 10 MB)
LOG_BACKUP_COUNT = os.getenv("LOG_BACKUP_COUNT")  # Number of backup log files

# Trading parameters
TRADING_PAIRS = ["BTCUSDT", "ETHUSDT"]  # Trading pairs to monitor
BASE_CURRENCY = "USDT"  # Base currency for trading
QUOTE_CURRENCIES = ["BTC", "ETH"]  # Quote currencies for trading

# Position sizing and risk management
MAX_POSITION_SIZE = 0.01  # Maximum position size as a fraction of available balance
STOP_LOSS_PERCENT = 0.02  # Stop loss percentage
TAKE_PROFIT_PERCENT = 0.04  # Take profit percentage

# Trading timeframes
TIMEFRAMES = {
    "1m": "1m",  # 1 minute
    "5m": "5m",  # 5 minutes
    "15m": "15m",  # 15 minutes
    "30m": "30m",  # 30 minutes
    "1h": "1h",  # 1 hour
    "4h": "4h",  # 4 hours
    "1d": "1d",  # 1 day
}

# Default timeframe for analysis
DEFAULT_TIMEFRAME = TIMEFRAMES["5m"]

# Backtesting parameters
BACKTEST_START_DATE = "2025-01-01"  # Start date for backtesting
BACKTEST_END_DATE = "2025-04-01"  # End date for backtesting

# API request parameters
API_RATE_LIMIT = 1200  # Maximum number of requests per minute
REQUEST_TIMEOUT = 10  # Timeout for API requests in seconds

# Trading bot operation modes
MODE_BACKTEST = "backtest"  # Backtesting mode
MODE_PAPER = "paper"  # Paper trading mode
MODE_LIVE = "live"  # Live trading mode

# Default operation mode
DEFAULT_MODE = MODE_PAPER

# Trading strategy parameters
ALLOW_LONG_BUYING = True
ALLOW_SHORT_SELLING = True
