def classify(df):
    """
    Classify market regime using Hurst exponent,
    volatility regime, and volume spikes.
    """

    def get_regime(row):

        # Strong anomaly: high volatility + unusual participation
        if row["vol_regime"] == "HIGH" and row["volume_spike"]:
            return "ANOMALY"

        # Clean trend (persistent movement)
        elif row["hurst"] > 0.6 and row["vol_regime"] == "LOW":
            return "TRENDING"

        # weak trend (persistent but noisy)
        elif row["hurst"] > 0.6:
            return "WEAK_TREND"

        # mean reversion tendency
        elif row["hurst"] < 0.45:
            return "MEAN_REVERTING"

        # random walk behavior
        else:
            return "RANDOM"

    df["regime"] = df.apply(get_regime, axis=1)

    return df