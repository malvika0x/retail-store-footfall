# visualizer.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_daily_line(daily_df):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily_df["date"], daily_df["daily_visitors"], marker="o", linewidth=1.5)
    ax.set_xlabel("Date")
    ax.set_ylabel("Visitors")
    ax.set_title("Daily Total Visitors")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_day_of_week_bar(df):
    tmp = df.groupby("day_name")["visitors"].sum().reset_index()
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    tmp["day_name"] = pd.Categorical(tmp["day_name"], categories=order, ordered=True)
    tmp = tmp.sort_values("day_name")

    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=tmp, x="day_name", y="visitors", order=order, ax=ax)
    ax.set_xlabel("Day of Week")
    ax.set_ylabel("Total visitors")
    ax.set_title("Footfall by Day of Week")
    plt.xticks(rotation=30)
    plt.tight_layout()
    return fig


def plot_monthly_bar(monthly_df):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.bar(monthly_df["month"], monthly_df["monthly_visitors"])
    ax.set_xlabel("Month")
    ax.set_ylabel("Total visitors")
    ax.set_title("Monthly Total Visitors")
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig


def plot_hour_weekday_heatmap(heatmap1):
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.heatmap(heatmap1, cmap="YlOrRd", ax=ax)
    ax.set_xlabel("Hour of Day")
    ax.set_ylabel("Day of Week")
    ax.set_title("Average Visitors: Hour vs Day of Week")
    plt.tight_layout()
    return fig


def plot_month_day_heatmap(heatmap2):
    fig, ax = plt.subplots(figsize=(12, 4))
    sns.heatmap(heatmap2, cmap="Blues", ax=ax)
    ax.set_xlabel("Day of Month")
    ax.set_ylabel("Month")
    ax.set_title("Average Visitors: Month vs Day of Month")
    plt.tight_layout()
    return fig


def plot_forecast(history_pred_df, future_pred_df):
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(
        history_pred_df["date"],
        history_pred_df["actual"],
        label="Actual",
        marker="o",
        linewidth=1,
    )
    ax.plot(
        history_pred_df["date"],
        history_pred_df["predicted"],
        label="Fitted trend",
        linewidth=2,
    )
    ax.plot(
        future_pred_df["date"],
        future_pred_df["predicted"],
        label="Forecast",
        linestyle="--",
        linewidth=2,
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Visitors")
    ax.set_title("Linear Trend Forecast of Daily Visitors")
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig
