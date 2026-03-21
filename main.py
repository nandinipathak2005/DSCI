# # import pandas as pd
# # import os
# # from src.data_loader import load_csv
# # from src.preprocessing import preprocess, add_session

# # def run(symbol):
# #     print(f"--- Starting {symbol} ---")
    
# #     # 1. Load
# #     df = load_csv(symbol) 
    
# #     # 2. Process
# #     df = preprocess(df)
# #     df = add_session(df)
    
# #     # 3. Save Output
# #     # Create the directory if it doesn't exist to prevent errors
# #     if not os.path.exists("outputs"):
# #         os.makedirs("outputs")
        
# #     output_path = f"outputs/{symbol}_processed.csv"
# #     df.to_csv(output_path, index=False)
    
# #     print(f"Successfully saved to {output_path}")

# # if __name__ == "__main__":
# #     stocks = ["RELIANCE", "TCS", "ADANIGREEN"]
# #     for s in stocks:
# #         try:
# #             run(s)
# #         except Exception as e:
# #             print(f"Error processing {s}: {e}")

# import pandas as pd
# import os
# # Import specifically the new function name
# from src.data_loader import load_data 
# from src.preprocessing import preprocess, add_session
# from src.features import add_features

# def run(symbol):
#     print(f"--- Starting {symbol} ---")
    
#     # 1. Load (This must match the import name above)
#     df = load_data(symbol)
    
#     # 2. Process
#     df = preprocess(df)
#     df = add_session(df)
    
#     # 3. Features
#     df = add_features(df)
    
#     # 4. Save
#     if not os.path.exists("outputs"):
#         os.makedirs("outputs")
        
#     output_path = f"outputs/{symbol}_processed.csv"
#     df.to_csv(output_path, index=False)
#     print(f"Successfully saved to {output_path}")

# if __name__ == "__main__":
#     # Use names that match your CSV files
#     stocks = ["RELIANCE", "TCS", "ADANIGREEN"]
    
#     for s in stocks:
#         try:
#             run(s)

#         except Exception as e:
#             print(f"Error on {s}: {e}")


import os
from src.data_loader import load_data
from src.preprocessing import preprocess, add_session
from src.features import add_features

def run(symbol, use_yfinance=False):
    print(f"--- Processing {symbol} ---")
    
    # Load CSV + optional live Yahoo Finance data
    df = load_data(symbol, use_yfinance=use_yfinance)
    print(f"Loaded {len(df)} rows for {symbol}")
    
    # Preprocess: sort, compute log returns, filter bad data
    df = preprocess(df)
    
    # Add session info (OPEN/MID/CLOSE)
    df = add_session(df)
    
    # Feature engineering: rolling mean, volatility, slope
    df = add_features(df)
    
    # Save processed CSV
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
    
    output_file = f"outputs/{symbol}_processed.csv"
    df.to_csv(output_file, index=False)
    print(f"Saved processed file to {output_file}\n")

if __name__ == "__main__":
    stocks = ["RELIANCE", "TCS", "ADANIGREEN"]
    
    for s in stocks:
        run(s, use_yfinance=True)