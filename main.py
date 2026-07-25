import os
from datetime import datetime, timedelta
from cleanDf import clean_dataframe
import pandas as pd
import requests
from downloader import update_master_data

from indicators import *
from screeners import *

# -----------------------------
# Configuration
# -----------------------------

DATA_FOLDER = "data"
TEMP_FOLDER = "temp"

MASTER_FILE = os.path.join(DATA_FOLDER, "nse_master.parquet")

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

START_DATE = datetime.today() - timedelta(days=730)
END_DATE = datetime.today()

# -----------------------------
# Create folders
# -----------------------------

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(TEMP_FOLDER, exist_ok=True)

# -----------------------------
# download / update & clean
# -----------------------------

market_data = update_master_data()


# Add indicators
market_data = add_sma(market_data, 20)
market_data = add_sma(market_data, 50)

market_data = add_ema(market_data, 20)

market_data = add_average_volume(market_data, 20)

market_data = add_daily_return(market_data)

market_data = add_rolling_high(market_data, 20)
market_data = add_rolling_low(market_data, 20)

today = market_data[
    market_data["DATE1"] == market_data["DATE1"].max()
]

result = price_range(today, 100, 500)

print("today result: ", result)

result = price_range(today, 100, 500)

result = volume_above(result, 2_000_000)

result = delivery_above(result, 60)

result = above_sma(result, 20)

result = breakout(result, 20)

print(result)