# retail-store-footfall

# Retail Footfall Analysis 🏪

## Overview
This project analyzes retail store traffic data to identify peak hours and weekly patterns. 

## How I Built It
I used **Pandas** for data manipulation and **Matplotlib** for the final visuals. The goal was to take raw timestamps and turn them into something a store manager could actually use.

## How to Run
1. Ensure you have `pandas`, `numpy`, and `matplotlib` installed.
2. Place your `data.csv` in the root folder.
3. Run `python analysis.py`.

## Data Logic
- **Peak Hours:** Calculated by counting unique visitor timestamps within 60-minute windows.
- **Heatmap:** Uses a pivot table to compare 'Day of Week' against 'Hour of Day'.

## Challenges Faced
- Sorting the days of the week (Monday-Sunday) was tricky because Python sorts them alphabetically by default. I solved this by using a categorical sort in Pandas.
