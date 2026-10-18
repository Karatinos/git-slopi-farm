import numpy as np
import pandas as pd

INPUT_PATH = "transactions.csv"
OUTPUT_PATH = "submission.csv"
RARE_CATEGORIES = {5964, 5967, 7994, 7995, 6051}


def percentile_rank(values):
    return pd.Series(values).rank(pct=True).to_numpy()


def build_score(df):
    dt = pd.to_datetime(df["timestamp"])
    hour = dt.dt.hour.to_numpy()
    amount = df["amount"].to_numpy(dtype=float)
    magnitude = np.abs(amount)

    home = df.groupby("user_id")["country"].transform(lambda s: s.mode().iloc[0])
    foreign = (df["country"].to_numpy() != home.to_numpy()).astype(float)
    night = (hour < 6).astype(float)
    rare = df["merchant_category"].isin(RARE_CATEGORIES).to_numpy().astype(float)
    unknown_device = (df["device_type"] == "unknown").to_numpy().astype(float)
    negative = (amount < 0).astype(float)
    large = (amount > 1000).astype(float)
    very_large = (amount > 5000).astype(float)

    order = np.argsort(dt.to_numpy(), kind="stable")
    seen = {}
    new_country = np.zeros(len(df))
    users = df["user_id"].to_numpy()
    countries = df["country"].to_numpy()
    for i in order:
        bucket = seen.setdefault(users[i], set())
        if bucket and countries[i] not in bucket:
            new_country[i] = 1.0
        bucket.add(countries[i])

    card_median = df.groupby("card_id")["amount"].transform(lambda s: s[s > 0].median())
    ratio = magnitude / (card_median.fillna(1.0).to_numpy(dtype=float) + 1.0)

    amount_rank = percentile_rank(np.log1p(np.clip(magnitude, 0.0, None)))
    ratio_rank = percentile_rank(ratio)

    evidence_a = (
        5.0 * negative
        + 2.0 * large
        + 1.0 * very_large
        + 1.2 * night
        + 1.0 * foreign
        + 1.2 * rare
        + 0.6 * unknown_device
        + 1.0 * large * night * foreign
        + 0.8 * large * rare
        + 0.5 * amount_rank
    )
    evidence_b = (
        amount_rank
        + 1.0 * night
        + 1.1 * foreign
        + 1.2 * rare
        + 0.5 * unknown_device
        + 0.7 * ratio_rank
        + 1.0 * new_country
        + 1.0 * night * foreign
        + 2.0 * negative
    )
    return 0.5 * percentile_rank(evidence_a) + 0.5 * percentile_rank(evidence_b)


def main():
    df = pd.read_csv(INPUT_PATH)
    score = build_score(df)
    submission = pd.DataFrame(
        {"transaction_id": df["transaction_id"].to_numpy(), "prediction": score}
    )
    submission.to_csv(OUTPUT_PATH, index=False)


if __name__ == "__main__":
    main()
