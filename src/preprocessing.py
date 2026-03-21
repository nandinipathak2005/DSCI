# # import numpy as np
# # import pandas as pd

# # def preprocess(df):
# #     # 1. Standard Cleanup & Sorting
# #     # Using .copy() prevents 'SettingWithCopy' warnings in Pandas
# #     df = df.dropna().copy()
# #     df = df.sort_values("Datetime")
    
# #     # Identify the correct close column (handles 'close' or 'Close')
# #     close_col = "close" if "close" in df.columns else "Close"
    
# #     # 2. Safety Check: Filter out rows where price is 0 or less to avoid log errors
# #     df = df[df[close_col] > 0].copy()
    
# #     # 3. Calculate Log Returns
# #     # Formula: ln(Price_t / Price_{t-1})
# #     df["returns"] = np.log(df[close_col] / df[close_col].shift(1))
    
# #     # 4. Final Cleanup
# #     # Replaces infinity (from div by 0) with NaN and drops them
# #     df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["returns"])
    
# #     return df

# # def add_session(df):
# #     """
# #     Categorizes trading time into OPEN, MID, or CLOSE sessions.
# #     """
# #     # Extract hour from the Datetime column
# #     df["hour"] = df["Datetime"].dt.hour

# #     def session_label(h):
# #         if h < 11:
# #             return "OPEN"
# #         elif h < 14:
# #             return "MID"
# #         else:
# #             return "CLOSE"

# #     df["session"] = df["hour"].apply(session_label)
# #     return df

# import numpy as np

# def preprocess(df):
#     # 1. Standard Cleanup
#     df = df.dropna().copy()
#     df = df.sort_values("Datetime")
    
#     # 2. Case-insensitive column finding
#     close_col = "close" if "close" in df.columns else "Close"
    
#     # 3. Safety: Filter out zero/negative prices
#     df = df[df[close_col] > 0].copy()
    
#     # 4. Calculate Log Returns
#     df["returns"] = np.log(df[close_col] / df[close_col].shift(1))
    
#     # 5. Final drop of Inf/NaN
#     df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=["returns"])
    
#     return df

# def add_session(df):
#     df["hour"] = df["Datetime"].dt.hour

#     def session_label(h):
#         if h < 11: return "OPEN"
#         elif h < 14: return "MID"
#         else: return "CLOSE"

#     df["session"] = df["hour"].apply(session_label)
#     return df

import numpy as np
import pandas as pd

def find_column(df, candidates):
    """Return the first column in df that matches any candidate name"""
    for c in candidates:
        for col in df.columns:
            col_name = col if isinstance(col, str) else col[0]  # handle tuples
            if c.lower() in str(col_name).lower():
                return col
    raise ValueError(f"No column found among {candidates}")

def preprocess(df):
    # Ensure columns are strings (or tuples)
    df.columns = [c if isinstance(c, tuple) else str(c) for c in df.columns]

    # Identify Close column
    close_col = find_column(df, ['Close', 'Adj Close', 'close', 'adj_close'])
    df = df[df[close_col] > 0].copy()

    # Identify datetime column
    dt_col = find_column(df, ['Datetime', 'Date', 'datetime', 'date'])
    df = df.sort_values(dt_col).copy()

    # Compute log returns
    df['returns'] = np.log(df[close_col] / df[close_col].shift(1))
    df = df.replace([np.inf, -np.inf], np.nan).dropna(subset=['returns'])

    # Rename datetime to standard
    df['Datetime'] = pd.to_datetime(df[dt_col])

    return df

def add_session(df):
    df['hour'] = df['Datetime'].dt.hour

    def session_label(h):
        if h < 11:
            return 'OPEN'
        elif h < 14:
            return 'MID'
        else:
            return 'CLOSE'

    df['session'] = df['hour'].apply(session_label)
    return df