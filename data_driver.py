# data_driver.py
import numpy as np
import pandas as pd


def generate_footfall_data(
    start_date="2024-01-01",
    end_date="2024-12-31",
    store_open=9,
    store_close=21,
    base_visitors=30,
    noise_level=15,
):
   
    dt_range = pd.date_range(start=start_date, end=end_date, freq="H")
    df = pd.DataFrame({"timestamp": dt_range})

    df["hour"] = df["timestamp"].dt.hour
    df = df[(df["hour"] >= store_open) & (df["hour"] < store_close)]

    df["date"] = df["timestamp"].dt.date
    df["month"] = df["timestamp"].dt.to_period("M").astype(str)
    df["day_name"] = df["timestamp"].dt.day_name()
    df["day_of_month"] = df["timestamp"].dt.day
    df["is_weekend"] = df["day_name"].isin(["Saturday", "Sunday"])

    # Footfall pattern:
    hour = df["hour"].values
    morning_peak = np.exp(-0.5 * ((hour - 11) / 1.5) ** 2)
    afternoon_peak = np.exp(-0.5 * ((hour - 15) / 1.5) ** 2)
    evening_peak = np.exp(-0.5 * ((hour - 19) / 1.8) ** 2)

    pattern = morning_peak + 1.4 * afternoon_peak + 1.8 * evening_peak

    weekend_boost = np.where(df["is_weekend"], 1.3, 1.0)

    # Month seasonality
    month_idx = df["timestamp"].dt.month
    month_factor = 1 + 0.3 * np.sin((month_idx - 1) / 12 * 2 * np.pi)

    visitors = (
        base_visitors * pattern * weekend_boost * month_factor
        + np.random.normal(0, noise_level, size=len(df))
    )
    visitors = np.clip(visitors.round().astype(int), 0, None)

    df["visitors"] = visitors

    return df
