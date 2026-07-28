from backend.market.indicators import Indicators
import pandas as pd

# Sample price data
prices = pd.Series([10, 20, 30, 40, 50])

print("========== SMA ==========")
print(Indicators.sma(prices, 3))

print("\n========== EMA ==========")
print(Indicators.ema(prices, 3))