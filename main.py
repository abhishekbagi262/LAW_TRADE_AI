from backend.market.market_data import MarketData

market = MarketData()

data = market.get_stock_data("RELIANCE.NS")

print(data.tail())