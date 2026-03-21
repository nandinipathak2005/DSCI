# import numpy as np

# def add_features(df):
#     # Identify column
#     close_col = "close" if "close" in df.columns else "Close"

#     # 1. Rolling Mean (10-period)
#     df["rolling_mean"] = df[close_col].rolling(10).mean()
    
#     # 2. Volatility (10-period)
#     df["volatility"] = df["returns"].rolling(10).std()

#     # 3. Trend Slope
#     # Uses polyfit to find the direction of the price over the last 10 minutes
#     df["slope"] = df[close_col].rolling(10).apply(
#         lambda x: np.polyfit(range(len(x)), x, 1)[0]
#     )

#     return df.dropna()

import numpy as np
from .preprocessing import find_column

def add_features(df):
    close_col = find_column(df, ['Close', 'Adj Close', 'close', 'adj_close'])

    # Rolling mean
    df['rolling_mean'] = df[close_col].rolling(10).mean()

    # Rolling volatility
    df['volatility'] = df['returns'].rolling(10).std()

    # Trend slope
    df['slope'] = df[close_col].rolling(10).apply(
        lambda x: np.polyfit(range(len(x)), x, 1)[0]
    )

    return df