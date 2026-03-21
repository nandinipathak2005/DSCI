# import numpy as np

# def find_close_column(df):
#     for col in df.columns:
#         if "close" in col.lower():
#             return col
#     raise ValueError("No Close column found")


# def hurst(ts):
#     lags = range(2, 20)

#     tau = []
#     for lag in lags:
#         diff = ts[lag:] - ts[:-lag]
#         tau.append(np.std(diff))

#     tau = np.array(tau)

#     if np.any(tau <= 0):
#         return np.nan

#     poly = np.polyfit(np.log(lags), np.log(tau), 1)
#     return poly[0]


# def rolling_hurst(df):
#     close_col = find_close_column(df)

#     df["hurst"] = df[close_col].rolling(50).apply(
#         lambda x: hurst(x) if len(x.dropna()) > 20 else np.nan
#     )

#     return df

import numpy as np

def find_close_column(df):
    for col in df.columns:
        if "close" in col.lower():
            return col
    raise ValueError("No Close column found")


def hurst(ts):
    ts = np.array(ts)

    lags = range(2, 20)
    tau = []

    for lag in lags:
        diff = ts[lag:] - ts[:-lag]
        tau.append(np.std(diff))

    tau = np.array(tau)

    if np.any(tau <= 0):
        return np.nan

    poly = np.polyfit(np.log(lags), np.log(tau), 1)
    return poly[0]


def rolling_hurst(df):
    close_col = find_close_column(df)

    prices = df[close_col].values
    hurst_vals = np.full(len(prices), np.nan)

    window = 30

    # 🔥 manual loop (MUCH faster than pandas rolling.apply)
    for i in range(window, len(prices)):
        window_data = prices[i-window:i]

        if np.isnan(window_data).any():
            continue

        hurst_vals[i] = hurst(window_data)

    df["hurst"] = hurst_vals

    return df