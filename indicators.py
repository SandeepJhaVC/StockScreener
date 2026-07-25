# --------------------------------------------------
# Moving Averages
# --------------------------------------------------

def add_sma(df, period):
    """
    Adds Simple Moving Average.
    """

    df[f"SMA_{period}"] = (
        df.groupby("SYMBOL")["CLOSE_PRICE"]
        .transform(lambda x: x.rolling(period).mean())
    )

    return df


def add_ema(df, period):
    """
    Adds Exponential Moving Average.
    """

    df[f"EMA_{period}"] = (
        df.groupby("SYMBOL")["CLOSE_PRICE"]
        .transform(lambda x: x.ewm(span=period, adjust=False).mean())
    )

    return df


# --------------------------------------------------
# Returns
# --------------------------------------------------

def add_daily_return(df):
    """
    Daily percentage return.
    """

    df["DAILY_RETURN"] = (
        (df["CLOSE_PRICE"] - df["PREV_CLOSE"])
        / df["PREV_CLOSE"]
    ) * 100

    return df


# --------------------------------------------------
# Volume Indicators
# --------------------------------------------------

def add_average_volume(df, period=20):
    """
    Rolling average volume.
    """

    df[f"AVG_VOLUME_{period}"] = (
        df.groupby("SYMBOL")["TTL_TRD_QNTY"]
        .transform(lambda x: x.rolling(period).mean())
    )

    return df


# --------------------------------------------------
# Highs and Lows
# --------------------------------------------------

def add_rolling_high(df, period):
    """
    Highest HIGH_PRICE in previous 'period' days.
    """

    df[f"HIGH_{period}"] = (
        df.groupby("SYMBOL")["HIGH_PRICE"]
        .transform(lambda x: x.rolling(period).max())
    )

    return df


def add_rolling_low(df, period):
    """
    Lowest LOW_PRICE in previous 'period' days.
    """

    df[f"LOW_{period}"] = (
        df.groupby("SYMBOL")["LOW_PRICE"]
        .transform(lambda x: x.rolling(period).min())
    )

    return df


# --------------------------------------------------
# Delivery
# --------------------------------------------------

def add_average_delivery(df, period=20):
    """
    Average delivery percentage.
    """

    df[f"AVG_DELIVERY_{period}"] = (
        df.groupby("SYMBOL")["DELIV_PER"]
        .transform(lambda x: x.rolling(period).mean())
    )

    return df

def above_sma(df, period):
    return df[
        df["CLOSE_PRICE"] > df[f"SMA_{period}"]
    ]


def below_sma(df, period):
    return df[
        df["CLOSE_PRICE"] < df[f"SMA_{period}"]
    ]


def above_ema(df, period):
    return df[
        df["CLOSE_PRICE"] > df[f"EMA_{period}"]
    ]


def volume_spike(df, period=20, multiplier=2):
    return df[
        df["TTL_TRD_QNTY"] >
        multiplier * df[f"AVG_VOLUME_{period}"]
    ]


def breakout(df, period=20):
    return df[
        df["CLOSE_PRICE"] >
        df[f"HIGH_{period}"]
    ]


def breakdown(df, period=20):
    return df[
        df["CLOSE_PRICE"] <
        df[f"LOW_{period}"]
    ]


def positive_return(df):
    return df[
        df["DAILY_RETURN"] > 0
    ]


def negative_return(df):
    return df[
        df["DAILY_RETURN"] < 0
    ]