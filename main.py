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

# -----------------------------
# indicators
# -----------------------------

market_data = add_sma(market_data, 20)
market_data = add_sma(market_data, 50)
market_data = add_ema(market_data, 20)
market_data = add_ema(market_data, 50)
market_data = add_daily_return(market_data)
market_data = add_average_volume(market_data, period=20)
market_data = add_rolling_high(market_data, period=20)
market_data = add_rolling_low(market_data, period=20)
market_data = add_average_delivery(market_data, period=20)

# -----------------------------
# screeners on whole dataset
# -----------------------------

if market_data.empty:
    print("No market data available after update.")
else:
    first_date = market_data["DATE1"].min()
    last_date = market_data["DATE1"].max()

    print(f"Data range: {first_date.date()} to {last_date.date()}")
    print(f"Total rows in dataset: {len(market_data)}")
    print("\nFull dataset sample:")
    print(market_data[["SYMBOL", "DATE1", "OPEN_PRICE", "CLOSE_PRICE", "PREV_CLOSE", "TTL_TRD_QNTY", "SMA_20", "EMA_20", "DAILY_RETURN"]].head(5))

    bullish = bullish_candle(market_data)
    high_volume = volume_above(market_data, 1_000_000)
    above_sma_20 = above_sma(market_data, 20)
    positive = positive_return(market_data)
    close_high = close_at_high(market_data)
    gap_up_symbols = gap_up(market_data)

    print("\nScreener counts across full dataset:")
    print(f"Bullish candles: {len(bullish)}")
    print(f"High volume (>1,000,000): {len(high_volume)}")
    print(f"Above SMA 20: {len(above_sma_20)}")
    print(f"Positive return: {len(positive)}")
    print(f"Close at high: {len(close_high)}")
    print(f"Gap up: {len(gap_up_symbols)}")

    if not bullish.empty:
        print("\nSample bullish rows:")
        print(bullish[["SYMBOL", "DATE1", "CLOSE_PRICE", "OPEN_PRICE"]].head(5).to_string(index=False))

    if not above_sma_20.empty:
        print("\nSample rows above SMA 20:")
        print(above_sma_20[["SYMBOL", "DATE1", "CLOSE_PRICE", "SMA_20"]].head(5).to_string(index=False))

    if not close_high.empty:
        print("\nSample close-at-high rows:")
        print(close_high[["SYMBOL", "DATE1", "CLOSE_PRICE", "HIGH_PRICE"]].head(5).to_string(index=False))
