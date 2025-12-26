# analysis.py
import pandas as pd
from sklearn.linear_model import LinearRegression


def compute_daily_stats(df):
    daily = (
        df.groupby("date")["visitors"]
        .sum()
        .reset_index()
        .rename(columns={"visitors": "daily_visitors"})
    )
    daily["date"] = pd.to_datetime(daily["date"])
    return daily


def compute_monthly_stats(df):
    df_copy = df.copy()
    df_copy["date"] = pd.to_datetime(df_copy["date"])
    df_copy.set_index("date", inplace=True)

    monthly = (
        df_copy["visitors"]
        .resample("M")
        .sum()
        .reset_index()
        .rename(columns={"visitors": "monthly_visitors"})
    )
    monthly["month"] = monthly["date"].dt.to_period("M").astype(str)
    return monthly


def build_heatmap_hour_weekday(df):
    pivot = df.pivot_table(
        index="day_name",
        columns="hour",
        values="visitors",
        aggfunc="mean",
    )
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex(order)
    return pivot


def build_heatmap_month_day(df):
    pivot = df.pivot_table(
        index="month",
        columns="day_of_month",
        values="visitors",
        aggfunc="mean",
    )
    pivot = pivot.sort_index()
    return pivot


def fit_daily_regression(daily_df, horizon_days=30):
    daily_df = daily_df.sort_values("date").reset_index(drop=True)
    daily_df["t"] = (daily_df["date"] - daily_df["date"].min()).dt.days

    X = daily_df[["t"]].values
    y = daily_df["daily_visitors"].values

    model = LinearRegression()
    model.fit(X, y)

    last_t = daily_df["t"].max()
    future_t = range(last_t + 1, last_t + 1 + horizon_days)
    future_t = list(future_t)

    future_dates = daily_df["date"].max() + pd.to_timedelta(
        [ft - last_t for ft in future_t], unit="D"
    )

    y_pred_future = model.predict([[ft] for ft in future_t])
    y_pred = model.predict(X)

    history_pred_df = pd.DataFrame(
        {"date": daily_df["date"], "actual": y, "predicted": y_pred}
    )

    future_pred_df = pd.DataFrame(
        {"date": future_dates, "predicted": y_pred_future}
    )

    return model, history_pred_df, future_pred_df
