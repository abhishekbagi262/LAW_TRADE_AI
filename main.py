from backend.market.market_data import MarketData

market = MarketData()

symbol = input("Enter Stock Symbol: ").upper()

price = market.get_current_price(symbol)

if price:
    print(f"\nCurrent Price of {symbol}: ₹{price}")
else:
    print("Invalid stock symbol.")