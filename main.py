from backend.market.market_data import MarketData
from backend.market.technical_analysis import TechnicalAnalysis


market = MarketData()
technical = TechnicalAnalysis()

symbol = input("Enter Stock Symbol: ").upper()

price = market.get_current_price(symbol)
change = market.get_day_change(symbol)
info = market.get_company_info(symbol)
analysis = market.get_analysis_data(symbol)
technical_data = technical.get_technical_analysis(symbol)

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

    print("\n========== TECHNICAL ANALYSIS ==========\n")

    if technical_data:

        print(f"20-Day SMA      : ₹{technical_data['sma_20']}")
        print(f"50-Day SMA      : ₹{technical_data['sma_50']}")
        print(f"RSI             : {technical_data['rsi']}")
        print(f"RSI Signal      : {technical_data['rsi_signal']}")
        print(f"MACD            : {technical_data['macd']}")
        print(f"MACD Signal     : {technical_data['macd_signal']}")
        print(f"MACD Trend      : {technical_data['macd_trend']}")
        print(f"Market Trend    : {technical_data['trend']}")

    else:
        print("Technical data unavailable.")

else:
    print("Invalid stock symbol.")