import pandas as pd
def clean_dataframe(df):

    # Clean column names
    df.columns = df.columns.str.strip()

    # Clean string values
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.strip()

    # Keep only equity rows if the SERIES column exists
    if "SERIES" in df.columns:
        df = df[df["SERIES"].astype(str).str.upper() == "EQ"]
    elif "series" in df.columns:
        df = df[df["series"].astype(str).str.upper() == "EQ"]

    # Convert date
    df["DATE1"] = pd.to_datetime(df["DATE1"], errors="coerce")

    numeric_columns = [
        "PREV_CLOSE",
        "OPEN_PRICE",
        "HIGH_PRICE",
        "LOW_PRICE",
        "LAST_PRICE",
        "CLOSE_PRICE",
        "AVG_PRICE",
        "TTL_TRD_QNTY",
        "TURNOVER_LACS",
        "NO_OF_TRADES",
        "DELIV_QTY",
        "DELIV_PER"
    ]

    for col in numeric_columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.strip()
        )

        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df