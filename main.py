from backend.market.market_data import MarketData

market = MarketData()

symbol = input("Enter Stock Symbol: ").upper()

price = market.get_current_price(symbol)
change = market.get_day_change(symbol)
info = market.get_company_info(symbol)
financials = market.get_financials(symbol)
balance_sheet = market.get_balance_sheet(symbol)
cashflow = market.get_cashflow(symbol)
pe_ratio = market.get_pe_ratio(symbol)

print("\n========== LAW TRADE AI ==========\n")

if price:
    print(f"Company : {info.get('longName', 'N/A')}")
    print(f"Symbol  : {symbol}")
    print(f"Price   : ₹{price}")
    print(f"Day Chg : {change}%")
    print(f"Sector  : {info.get('sector', 'N/A')}")
    print(f"Industry: {info.get('industry', 'N/A')}")
    print(f"P/E Ratio: {pe_ratio}")


    print("\nFinancial Data:")
    print(financials.head())
    print("\nBalance Sheet:")
    print(balance_sheet.head())
    print("\nCash Flow:")
    print(cashflow.head())
else:
    print("Invalid stock symbol.")