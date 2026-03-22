import numpy as np


def compute_confidence(df):
    """
    Confidence score indicates how strongly
    signals support a regime classification.
    """

    eps = 1e-9

    # Trend persistence strength
    df["hurst_strength"] = abs(df["hurst"] - 0.5)

    # volatility contribution
    df["vol_strength"] = (
        df["volatility"] /
        (df["volatility"].max() + eps)
    )

    df["vol_strength"] = df["vol_strength"].fillna(0)

    # volume anomaly strength
    df["vol_spike_strength"] = (
        abs(df["vol_z"]) /
        (abs(df["vol_z"]).max() + eps)
    )

    df["vol_spike_strength"] = df["vol_spike_strength"].fillna(0)

    # final confidence score
    df["confidence"] = (
        df["hurst_strength"] +
        df["vol_strength"] +
        df["vol_spike_strength"]
    ) / 3

    return df


def compute_risk(df):
    """
    Risk increases when volatility and
    volume anomalies increase.
    """

    eps = 1e-9

    df["risk"] = (
        df["volatility"] /
        (df["volatility"].max() + eps)
        +
        abs(df["vol_z"]) /
        (abs(df["vol_z"]).max() + eps)
    ) / 2

    return df