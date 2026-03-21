# # import pandas as pd
# # import os

# # SECTOR_INFO = {
# #     "RELIANCE": {"sector": "Energy", "market_cap": "Large"},
# #     "TCS": {"sector": "IT", "market_cap": "Large"},
# #     "ADANIGREEN": {"sector": "Energy", "market_cap": "Mid"},
# #     "HDFCBANK": {"sector": "Banking", "market_cap": "Large"},
# #     "BAJAJ-AUTO": {"sector": "Auto", "market_cap": "Mid"},
# # }

# # def load_csv(symbol, folder="data"):
# #     file_path = f"{folder}/{symbol}.csv"
    
# #     if not os.path.exists(file_path):
# #         raise FileNotFoundError(f"Could not find {file_path}")

# #     df = pd.read_csv(file_path)

# #     # Standardize the date column: Look for 'date' or 'Datetime'
# #     if "date" in df.columns:
# #         df = df.rename(columns={"date": "Datetime"})
    
# #     # Convert to actual datetime objects
# #     df["Datetime"] = pd.to_datetime(df["Datetime"])
    
# #     # Attach sector & market cap
# #     info = SECTOR_INFO.get(symbol, {"sector": "Unknown", "market_cap": "Unknown"})
# #     df["sector"] = info["sector"]
# #     df["market_cap"] = info["market_cap"]
    
# #     return df

# import pandas as pd
# import yfinance as yf
# import os

# SECTOR_INFO = {
#     "RELIANCE": {"sector": "Energy", "market_cap": "Large"},
#     "TCS": {"sector": "IT", "market_cap": "Large"},
#     "ADANIGREEN": {"sector": "Energy", "market_cap": "Mid"},
#     "HDFCBANK": {"sector": "Banking", "market_cap": "Large"},
#     "BAJAJ-AUTO": {"sector": "Auto", "market_cap": "Mid"},
# }

# def load_data(symbol, folder="data"):
#     """
#     Hybrid Loader: Checks local CSV first, then yfinance.
#     """
#     file_path = f"{folder}/{symbol}.csv"
    
#     # 1. Try to load local CSV
#     if os.path.exists(file_path):
#         print(f"Loading {symbol} from local CSV...")
#         df = pd.read_csv(file_path)
#         # Standardize local column names (your CSVs use 'date')
#         if "date" in df.columns:
#             df = df.rename(columns={"date": "Datetime"})
    
#     # 2. If no CSV, fetch from yfinance
#     else:
#         print(f"Local file not found. Fetching {symbol} from yfinance...")
#         yf_symbol = f"{symbol}.NS" if ".NS" not in symbol else symbol
#         df = yf.download(yf_symbol, interval="1m", period="1d")
#         df.reset_index(inplace=True)
    
#     # 3. Final Standardization
#     df["Datetime"] = pd.to_datetime(df["Datetime"])
    
#     # Attach metadata
#     clean_symbol = symbol.replace(".NS", "")
#     info = SECTOR_INFO.get(clean_symbol, {"sector": "Unknown", "market_cap": "Unknown"})
#     df["sector"] = info["sector"]
#     df["market_cap"] = info["market_cap"]
    
#     return df


# import pandas as pd
# import yfinance as yf

# # Optional: sector & market cap info for report / categorization
# SECTOR_INFO = {
#     "RELIANCE": {"sector": "Energy", "market_cap": "Large"},
#     "TCS": {"sector": "IT", "market_cap": "Large"},
#     "ADANIGREEN": {"sector": "Energy", "market_cap": "Mid"},
#     "HDFCBANK": {"sector": "Banking", "market_cap": "Large"},
#     "BAJAJ-AUTO": {"sector": "Auto", "market_cap": "Mid"},
#     # Add more as needed
# }

# def load_csv(symbol, folder="data"):
#     """Load historical CSV (Kaggle/NSE)"""
#     df = pd.read_csv(f"{folder}/{symbol}.csv")
#     df["Datetime"] = pd.to_datetime(df["Datetime"])
    
#     # Add sector info
#     info = SECTOR_INFO.get(symbol, {"sector": "Unknown", "market_cap": "Unknown"})
#     df["sector"] = info["sector"]
#     df["market_cap"] = info["market_cap"]
    
#     return df

# def fetch_yfinance(symbol, period="5d", interval="1m"):
#     """Fetch recent data from Yahoo Finance"""
#     df = yf.download(symbol + ".NS", period=period, interval=interval)
#     df.reset_index(inplace=True)
#     df["Datetime"] = pd.to_datetime(df["Datetime"])
    
#     info = SECTOR_INFO.get(symbol, {"sector": "Unknown", "market_cap": "Unknown"})
#     df["sector"] = info["sector"]
#     df["market_cap"] = info["market_cap"]
    
#     return df

# def load_data(symbol, folder="data", use_yfinance=False):
#     """Load CSV + optional Yahoo data"""
#     df = load_csv(symbol, folder)
    
#     if use_yfinance:
#         live = fetch_yfinance(symbol)
#         df = pd.concat([df, live], ignore_index=True)
#         df = df.drop_duplicates(subset="Datetime").sort_values("Datetime").reset_index(drop=True)
    
#     return df


import pandas as pd
import yfinance as yf

# Optional: sector info
SECTOR_INFO = {
    "RELIANCE": {"sector": "Energy", "market_cap": "Large"},
    "TCS": {"sector": "IT", "market_cap": "Large"},
    "ADANIGREEN": {"sector": "Energy", "market_cap": "Mid"},
}

def flatten_columns(df):
    """Flatten MultiIndex columns from yfinance to single-level strings"""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ["_".join([str(i) for i in col if i]).strip() for col in df.columns]
    else:
        df.columns = [str(c) for c in df.columns]
    return df

def load_csv(symbol, folder="data"):
    df = pd.read_csv(f"{folder}/{symbol}.csv")
    df = flatten_columns(df)
    return df

def fetch_yfinance(symbol, period="5d", interval="1m"):
    df = yf.download(symbol + ".NS", period=period, interval=interval)
    df.reset_index(inplace=True)
    df = flatten_columns(df)
    return df

def load_data(symbol, folder="data", use_yfinance=False):
    df = load_csv(symbol, folder)

    if use_yfinance:
        live = fetch_yfinance(symbol)
        df = pd.concat([df, live], ignore_index=True)
        # Flatten columns again to be safe
        df = flatten_columns(df)

        # Identify datetime column (first column containing date/datetime)
        dt_cols = [c for c in df.columns if "date" in c.lower() or "datetime" in c.lower()]
        if dt_cols:
            dt_col = dt_cols[0]
            df = df.drop_duplicates(subset=dt_col).sort_values(by=dt_col).reset_index(drop=True)
        else:
            # fallback
            df = df.drop_duplicates().reset_index(drop=True)

    # Add sector info
    info = SECTOR_INFO.get(symbol, {"sector": "Unknown", "market_cap": "Unknown"})
    df["sector"] = info["sector"]
    df["market_cap"] = info["market_cap"]

    return df