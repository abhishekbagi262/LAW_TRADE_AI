from backend.market.market_data import MarketData

market = MarketData()

symbol = input("Enter Stock Symbol: ").upper()

price = market.get_current_price(symbol)
change = market.get_day_change(symbol)
info = market.get_company_info(symbol)

print("\n========== LAW TRADE AI ==========\n")

if price:
    print(f"Company : {info.get('longName', 'N/A')}")
    print(f"Symbol  : {symbol}")
    print(f"Price   : ₹{price}")
    print(f"Day Chg : {change}%")
    print(f"Sector  : {info.get('sector', 'N/A')}")
    print(f"Industry: {info.get('industry', 'N/A')}")
else:
    print("Invalid stock symbol.")