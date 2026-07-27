import requests
import os
import pandas as pd
from datetime import datetime, timedelta
from cleanDf import clean_dataframe

DATA_FOLDER = "data"
TEMP_FOLDER = "temp"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

MASTER_FILE = os.path.join(DATA_FOLDER, "nse_master.parquet")

def load_master_data():
    if os.path.exists(MASTER_FILE):
        return pd.read_parquet(MASTER_FILE)

    return pd.DataFrame()

def get_last_date(df):

    if df.empty:
        return None

    return df["DATE1"].max()


def is_master_data_up_to_date():
    master_df = load_master_data()
    last_date = get_last_date(master_df)

    if last_date is None:
        return False

    return last_date.date() >= datetime.today().date()

def download_bhavcopy(date):

    filename = f"sec_bhavdata_full_{date.strftime('%d%m%Y')}.csv"

    url = f"https://nsearchives.nseindia.com/products/content/{filename}"

    temp_path = os.path.join(TEMP_FOLDER, filename)

    try:

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=20
        )

        if response.status_code != 200:
            return None

        with open(temp_path, "wb") as file:
            file.write(response.content)

        df = pd.read_csv(temp_path)

        os.remove(temp_path)

        return df

    except Exception as e:

        print(f"❌ Error downloading {filename}")

        print(e)

        return None

def update_master_data():

    master_df = load_master_data()

    last_date = get_last_date(master_df)

    if last_date is None:
        # First run: download 2 years of data
        current_date = datetime.today() - timedelta(days=730)
        end_date = datetime.today()
    else:
        # Already have data; continue from the next date
        current_date = last_date + timedelta(days=1)
        end_date = datetime.today()

    new_data = []

    while current_date <= end_date:

        print(f"Checking {current_date.date()}")

        df = download_bhavcopy(current_date)

        if df is not None:

            # Clean columns here if needed
            # df.columns = df.columns.str.strip()
            # df = clean_dataframe(df)

            new_data.append(df)

            print("Downloaded")

        current_date += timedelta(days=1)

    if new_data:

        new_df = pd.concat(new_data, ignore_index=True)
        new_df = clean_dataframe(new_df)

        new_df["DATE1"] = pd.to_datetime(new_df["DATE1"])

        master_df = pd.concat(
            [master_df, new_df],
            ignore_index=True
        )

        master_df.drop_duplicates(
            subset=["SYMBOL", "DATE1"],
            inplace=True
        )

        master_df.sort_values(
            ["SYMBOL", "DATE1"],
            inplace=True
        )

        # master_df = clean_dataframe(master_df)

        master_df.to_parquet(MASTER_FILE, index=False)

        print(f"Added {len(new_df)} rows.")

    else:
        print("Already up to date.")

    return master_df