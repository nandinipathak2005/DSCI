import numpy as np

def find_volume_column(df):
    for col in df.columns:
        if "volume" in col.lower():
            return col
    return None


def volume_features(df):

    vol_col = find_volume_column(df)

    # If no volume column, create dummy
    if vol_col is None:
        df["vol_z"] = 0
        df["volume_spike"] = False
        return df

    mean = df[vol_col].rolling(10).mean()
    std = df[vol_col].rolling(10).std()

    df["vol_z"] = (df[vol_col] - mean) / std
    df["vol_z"] = df["vol_z"].replace([np.inf, -np.inf], 0).fillna(0)

    df["volume_spike"] = df["vol_z"] > 2

    return df