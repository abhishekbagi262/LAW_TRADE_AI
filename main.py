from backend.market.market_data import MarketData


market = MarketData()

symbol = input("Enter Stock Symbol: ").upper()

price = market.get_current_price(symbol)
change = market.get_day_change(symbol)
info = market.get_company_info(symbol)
analysis = market.get_analysis_data(symbol)

print("\n========== LAW TRADE AI ==========\n")

if price:

    print(f"Company : {info.get('longName', 'N/A')}")
    print(f"Symbol  : {symbol}")
    print(f"Price   : ₹{price}")
    print(f"Day Chg : {change}%")
    print(f"Sector  : {info.get('sector', 'N/A')}")
    print(f"Industry: {info.get('industry', 'N/A')}")

    print("\n========== FUNDAMENTAL ANALYSIS ==========\n")

    print(f"P/E Ratio       : {info.get('trailingPE', 'N/A')}")
    print(f"EPS             : ₹{info.get('trailingEps', 'N/A')}")
    print(f"Profit Margin   : {analysis['profit_margin']}")
    print(f"ROE             : {analysis['roe']}")
    print(f"Debt/Equity     : {analysis['debt_to_equity']}")
    print(f"Revenue Growth  : {analysis['revenue_growth']}")
    print(f"Earnings Growth : {analysis['earnings_growth']}")
    print(f"Free Cash Flow  : {analysis['free_cash_flow']}")
    print(f"Dividend Yield  : {analysis['dividend_yield']}")
    print(f"Market Cap      : {analysis['market_cap']}")

else:
    print("Invalid stock symbol.")