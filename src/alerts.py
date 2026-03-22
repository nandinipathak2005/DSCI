def generate_alerts(df, symbol):
    """
    Generate alerts when:
    1. regime changes
    2. volume spikes
    3. risk becomes high
    """

    alerts = []

    for i in range(1, len(df)):

        row = df.iloc[i]

        # REGIME SHIFT ALERT
        if df["regime"].iloc[i] != df["regime"].iloc[i-1]:

            alerts.append({
                "time": row["Datetime"],
                "symbol": symbol,
                "type": "REGIME SHIFT",
                "new_regime": row["regime"],
                "confidence": row["confidence"]
            })

        # VOLUME SPIKE ALERT
        if row["volume_spike"]:

            alerts.append({
                "time": row["Datetime"],
                "symbol": symbol,
                "type": "VOLUME SPIKE",
                "z_score": row["vol_z"],
                "risk": row["risk"]
            })

        # HIGH RISK ALERT
        if row["risk"] > 0.7:

            alerts.append({
                "time": row["Datetime"],
                "symbol": symbol,
                "type": "HIGH RISK",
                "risk_score": row["risk"],
                "regime": row["regime"]
            })

    return alerts