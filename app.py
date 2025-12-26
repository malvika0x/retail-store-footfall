# app.py
import pandas as pd
import streamlit as st

from data_driver import generate_footfall_data
from analysis import (
    compute_daily_stats,
    compute_monthly_stats,
    build_heatmap_hour_weekday,
    build_heatmap_month_day,
    fit_daily_regression,
)
from visualizer import (
    plot_daily_line,
    plot_day_of_week_bar,
    plot_monthly_bar,
    plot_hour_weekday_heatmap,
    plot_month_day_heatmap,
    plot_forecast,
)


def main():
    st.set_page_config(page_title="Retail Footfall Analytics", layout="wide")

    st.title("Retail Store Footfall Analytics Dashboard")

    st.markdown(
        "Interactive analysis of **daily**, **monthly**, and **hourly** footfall patterns "
        "with heatmaps and a simple trend-based forecast."
    )

    # Sidebar controls
    st.sidebar.header("Data & Model Settings")

    start_date = st.sidebar.date_input("Start date", value=pd.to_datetime("2024-01-01"))
    end_date = st.sidebar.date_input("End date", value=pd.to_datetime("2024-12-31"))

    if start_date >= end_date:
        st.error("Start date must be before end date.")
        return

    base_visitors = st.sidebar.slider("Base visitors", 10, 100, 35, step=5)
    noise_level = st.sidebar.slider("Noise level", 0, 50, 15, step=5)
    forecast_horizon = st.sidebar.slider("Forecast horizon (days)", 7, 90, 30, step=7)

    st.sidebar.markdown("---")
    st.sidebar.write("Adjust the sliders and dates to regenerate synthetic data.")

    # Generate data
    df = generate_footfall_data(
        start_date=start_date,
        end_date=end_date,
        base_visitors=base_visitors,
        noise_level=noise_level,
    )

    # Aggregations
    daily_df = compute_daily_stats(df)
    monthly_df = compute_monthly_stats(df)

    # Top metrics
    total_visitors = int(daily_df["daily_visitors"].sum())
    avg_daily = float(daily_df["daily_visitors"].mean())
    best_day = daily_df.loc[daily_df["daily_visitors"].idxmax(), "date"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total visitors", f"{total_visitors:,}")
    col2.metric("Avg daily visitors", f"{avg_daily:,.0f}")
    col3.metric("Busiest day", best_day.strftime("%Y-%m-%d"))

    # Tabs
    tab_daily, tab_monthly, tab_heatmaps, tab_forecast, tab_raw = st.tabs(
        ["Daily Analysis", "Monthly Analysis", "Heatmaps", "Forecast", "Raw Data"]
    )

    # DAILY TAB
    with tab_daily:
        st.subheader("Daily Footfall Over Time")
        st.pyplot(plot_daily_line(daily_df))

        st.subheader("Average Daily Visitors by Day of Week")
        st.pyplot(plot_day_of_week_bar(df))

    # MONTHLY TAB
    with tab_monthly:
        st.subheader("Monthly Footfall")
        st.pyplot(plot_monthly_bar(monthly_df))
        st.dataframe(monthly_df[["month", "monthly_visitors"]])

    # HEATMAPS TAB
    with tab_heatmaps:
        st.subheader("Hourly vs Day-of-Week Heatmap")
        heatmap1 = build_heatmap_hour_weekday(df)
        st.pyplot(plot_hour_weekday_heatmap(heatmap1))

        st.subheader("Month vs Day-of-Month Heatmap")
        heatmap2 = build_heatmap_month_day(df)
        st.pyplot(plot_month_day_heatmap(heatmap2))

    # FORECAST TAB
    with tab_forecast:
        st.subheader("Daily Trend & Simple Forecast")
        _, history_pred_df, future_pred_df = fit_daily_regression(
            daily_df, horizon_days=forecast_horizon
        )
        st.pyplot(plot_forecast(history_pred_df, future_pred_df))

        st.write(
            "This forecast uses a simple linear regression on the daily totals "
            "with time index as the predictor."
        )

    # RAW DATA TAB
    with tab_raw:
        st.subheader("Sample of Raw Hourly Data")
        st.dataframe(df.head(200))


if __name__ == "__main__":
    main()
