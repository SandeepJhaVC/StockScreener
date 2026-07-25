def price_range(df, min_price, max_price):
    return df[
        (df["CLOSE_PRICE"] >= min_price) &
        (df["CLOSE_PRICE"] <= max_price)
    ]


def volume_above(df, volume):
    return df[
        df["TTL_TRD_QNTY"] >= volume
    ]


def turnover_above(df, turnover):
    return df[
        df["TURNOVER_LACS"] >= turnover
    ]


def delivery_above(df, delivery):
    return df[
        df["DELIV_PER"] >= delivery
    ]


def bullish_candle(df):
    return df[
        df["CLOSE_PRICE"] > df["OPEN_PRICE"]
    ]


def bearish_candle(df):
    return df[
        df["CLOSE_PRICE"] < df["OPEN_PRICE"]
    ]


def gap_up(df):
    return df[
        df["OPEN_PRICE"] > df["PREV_CLOSE"]
    ]


def gap_down(df):
    return df[
        df["OPEN_PRICE"] < df["PREV_CLOSE"]
    ]


def close_at_high(df):
    return df[
        df["CLOSE_PRICE"] == df["HIGH_PRICE"]
    ]


def close_at_low(df):
    return df[
        df["CLOSE_PRICE"] == df["LOW_PRICE"]
    ]
