def volatility_regime(df):
    mean = df["volatility"].mean()
    std = df["volatility"].std()

    df["vol_regime"] = df["volatility"].apply(
        lambda x: "HIGH" if x > (mean + std) else "LOW"
    )

    # Volatility clustering (boolean)
    df["vol_cluster"] = df["volatility"].rolling(5).mean() > mean

    return df