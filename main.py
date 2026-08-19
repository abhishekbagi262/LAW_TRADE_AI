from backend.market.market_data import MarketData
from backend.market.technical_analysis import TechnicalAnalysis
from backend.ai.decision_engine import DecisionEngine


market = MarketData()
technical = TechnicalAnalysis()
decision_engine = DecisionEngine()


symbol = input("Enter Stock Symbol: ").upper()


price = market.get_current_price(symbol)
change = market.get_day_change(symbol)
info = market.get_company_info(symbol)

analysis = market.get_analysis_data(symbol)
technical_data = technical.get_technical_analysis(symbol)


fundamental_data = {
    "pe_ratio": info.get("trailingPE"),
    "profit_margin": analysis.get("profit_margin"),
    "revenue_growth": analysis.get("revenue_growth"),
    "earnings_growth": analysis.get("earnings_growth")
}


decision = decision_engine.generate_signal(
    fundamental_data,
    technical_data
)


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
    print(f"Profit Margin   : {analysis.get('profit_margin')}")
    print(f"ROE             : {analysis.get('roe')}")
    print(f"Debt/Equity     : {analysis.get('debt_to_equity')}")
    print(f"Revenue Growth  : {analysis.get('revenue_growth')}")
    print(f"Earnings Growth : {analysis.get('earnings_growth')}")
    print(f"Free Cash Flow  : {analysis.get('free_cash_flow')}")
    print(f"Dividend Yield  : {analysis.get('dividend_yield')}")
    print(f"Market Cap      : {analysis.get('market_cap')}")


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


    print("\n========== LAW TRADE AI DECISION ==========\n")

    print(f"Score  : {decision['score']}")
    print(f"Signal : {decision['signal']}")

    print("\nReasons:")

    for reason in decision["reasons"]:
        print(f"- {reason}")


else:

    print("Invalid stock symbol.")
print("END")