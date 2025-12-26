# run_analysis.py
import matplotlib.pyplot as plt

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
    df = generate_footfall_data()
    daily_df = compute_daily_stats(df)
    monthly_df = compute_monthly_stats(df)

    # plots open in normal matplotlib windows
    fig1 = plot_daily_line(daily_df)
    fig2 = plot_day_of_week_bar(df)
    fig3 = plot_monthly_bar(monthly_df)

    heatmap1 = build_heatmap_hour_weekday(df)
    heatmap2 = build_heatmap_month_day(df)
    fig4 = plot_hour_weekday_heatmap(heatmap1)
    fig5 = plot_month_day_heatmap(heatmap2)

    _, history_pred_df, future_pred_df = fit_daily_regression(daily_df)
    fig6 = plot_forecast(history_pred_df, future_pred_df)

    plt.show()  # show all figures

if __name__ == "__main__":
    main()
