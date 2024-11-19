# Import required modules
import subprocess
import os
import runpy
import mplfinance
# Install mplfinance (if not already installed)
try:
    import mplfinance
except ImportError:
    print("Installing mplfinance...")
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", "mplfinance"])

# Define the notebook file and its converted script counterpart
notebook_file = "stock_analysis.ipynb"
script_file = "stock_analysis.py"

# Convert the .ipynb file to a .py file if needed
if not os.path.exists(script_file):
    try:
        print(f"Converting {notebook_file} to {script_file}...")
        subprocess.check_call(["jupyter", "nbconvert", "--to", "script", notebook_file])
    except Exception as e:
        print(f"Error converting notebook: {e}")
        exit(1)

# Simulate %run stock_analysis.ipynb by running the converted .py file
try:
    print(f"Running {script_file}...")
    runpy.run_path(script_file, run_name="_main_")
except Exception as e:
    print(f"Error running script: {e}")


with open('stock_analysis.ipynb', 'r') as file:
    print(file.read())

# %run stock_analysis.ipynb

import pandas as pd
import mplfinance as mpl
import numpy as np
import matplotlib.pyplot as plt

# Load and Inspect the Data:
# Load the dataset using pandas
df = pd.read_csv("infy_stock.csv")
# Display the first 10 rows of the dataset.
df.head(10)

# Check if there are any missing values and handle them appropriately.
df.isnull().sum()

df.ffill(inplace=True)
df["Date"] = pd.to_datetime(df["Date"])
df.set_index("Date", inplace=True)

# Data Visualization
# Plot the closing price over time.
df["Close"].plot()

df.index
df.shape

# Plot a candlestick chart for the stock prices (using mplfinance or another library of your choice)
mpl.plot(df.loc["2020-Jan-01":"2020-Jun-01", ['Open', 'High', 'Low', 'Close']], type='candle', volume=False, style='charles')

# Calculate the daily return percentage.
df["Return %age"] = ((df["Close"] - df["Open"])/df["Open"]) * 100

df[df["Return %age"] > 10]

# Calculate the average and median of daily returns.
# Calculate the standard deviation of the closing prices.
avg = df["Return %age"].sum()/df.shape[0]
mid = int((df.shape[0] + 1)/2)
median = df["Return %age"].sort_values().iloc[mid]
sd = (((df["Close"] - avg) * 2).sum()/df.shape[0]) * 0.5
print("Average return : ", avg)
print("Median return : ", median)
print("Standard Deviation of closing price : ", sd)

# Calculate the 50-day and 200-day moving averages of the stock's closing price and plot them.
df["50-day MA"] = df["Close"].rolling(window=50).mean()
df["200-day MA"] = df["Close"].rolling(window=200).mean()

df["50-day MA"].plot()
plt.xlabel('Date')
plt.ylabel('Moving Average')

df["200-day MA"].plot()
plt.xlabel('Date')
plt.ylabel('Moving Average')

# Volatility Analysis
# Plot the volatility of the stock using the rolling standard deviation (30-day window),
df["30-day sd"] = df["Close"].rolling(window=30).std(ddof=0)
df["30-day sd"].plot()
plt.xlabel('Date')
plt.ylabel('Standard Deviation')

# Trend Analysis
# Identify and mark the bullish and bearish trends based on moving averages (50-day vs 200-day)
df['Bullish'] = (df['50-day MA'] > df['200-day MA']) & (df['50-day MA'].shift(1) <= df['200-day MA'].shift(1))
bullish_points = df[df['Bullish']]
print(bullish_points[['Close', '50-day MA', '200-day MA']])

df[["50-day MA", "200-day MA"]].plot()

plt.plot(df.index, df['50-day MA'], label='50-day MA', color='blue')
plt.scatter(bullish_points.index, bullish_points['50-day MA'], marker='^', color='green', label='Bullish Crossover', s=50)