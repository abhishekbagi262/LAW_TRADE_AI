import streamlit as st

from backend.market.market_data import MarketData
from backend.market.technical_analysis import TechnicalAnalysis
from backend.ai.decision_engine import DecisionEngine
from backend.trading.paper_trading import PaperTrading


st.set_page_config(
    page_title="LAW TRADE AI",
    page_icon="📈",
    layout="wide"
)


# Initialize backend classes
market = MarketData()
technical = TechnicalAnalysis()
decision_engine = DecisionEngine()


# Initialize paper trader
if "paper_trader" not in st.session_state:
    st.session_state.paper_trader = PaperTrading(
        starting_balance=100000
    )


# Initialize analysis state
if "analysis" not in st.session_state:
    st.session_state.analysis = None


# Title
st.title("📈 LAW TRADE AI")
st.subheader("AI-Powered Stock Analysis System")


# Stock symbol input
symbol = st.text_input(
    "Enter Stock Symbol",
    "RELIANCE.NS"
).upper()


# Analyze button
if st.button("Analyze Stock"):

    with st.spinner("Analyzing stock..."):

        price = market.get_current_price(symbol)
        change = market.get_day_change(symbol)
        info = market.get_company_info(symbol)
        analysis = market.get_analysis_data(symbol)
        technical_data = technical.get_technical_analysis(symbol)


    if price is not None:

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


        st.session_state.analysis = {

            "symbol": symbol,
            "price": price,
            "change": change,
            "info": info,
            "analysis": analysis,
            "technical_data": technical_data,
            "decision": decision

        }


        st.success("Stock analyzed successfully!")


    else:

        st.error(
            "Invalid stock symbol or data unavailable."
        )


# Display analysis only after successful analysis
if st.session_state.analysis is not None:

    data = st.session_state.analysis


    analyzed_symbol = data["symbol"]
    price = data["price"]
    change = data["change"]
    info = data["info"]
    analysis = data["analysis"]
    technical_data = data["technical_data"]
    decision = data["decision"]


    st.success(
        f"{info.get('longName', 'N/A')} analyzed successfully"
    )


    # Stock Overview
    st.header("📌 Stock Overview")


    col1, col2, col3, col4 = st.columns(4)


    col1.metric(
        "Price",
        f"₹{price}"
    )


    col2.metric(
        "Day Change",
        f"{change}%"
    )


    col3.metric(
        "P/E Ratio",
        info.get("trailingPE", "N/A")
    )


    col4.metric(
        "EPS",
        f"₹{info.get('trailingEps', 'N/A')}"
    )


    # Price Chart
    st.header("📈 Price Chart")


    chart_data = market.get_stock_data(
        analyzed_symbol,
        period="6mo"
    )


    if not chart_data.empty:

        chart_data = chart_data[["Close"]].copy()


        if chart_data.index.tz is not None:

            chart_data.index = (
                chart_data.index.tz_localize(None)
            )


        st.line_chart(chart_data)


    # Fundamental Analysis
    st.header("📊 Fundamental Analysis")


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Profit Margin",
        analysis.get(
            "profit_margin",
            "N/A"
        )
    )


    col2.metric(
        "Revenue Growth",
        analysis.get(
            "revenue_growth",
            "N/A"
        )
    )


    col3.metric(
        "Earnings Growth",
        analysis.get(
            "earnings_growth",
            "N/A"
        )
    )


    # Technical Analysis
    st.header("📈 Technical Analysis")


    if technical_data:

        col1, col2, col3, col4 = st.columns(4)


        col1.metric(
            "20-Day SMA",
            f"₹{technical_data['sma_20']}"
        )


        col2.metric(
            "50-Day SMA",
            f"₹{technical_data['sma_50']}"
        )


        col3.metric(
            "RSI",
            technical_data["rsi"]
        )


        col4.metric(
            "Trend",
            technical_data["trend"]
        )


    # AI Decision
    st.header("🤖 LAW TRADE AI Decision")


    st.metric(
        "Final Signal",
        decision["signal"]
    )


    st.write(
        f"### Score: {decision['score']}"
    )


    st.subheader("AI Reasoning")


    for reason in decision["reasons"]:

        st.write(
            f"• {reason}"
        )


    # Paper Trading
    st.header("💰 Paper Trading")


    paper_trader = (
        st.session_state.paper_trader
    )


    st.metric(
        "Virtual Balance",
        f"₹{paper_trader.get_balance():,.2f}"
    )


    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1,
        step=1
    )


    col1, col2 = st.columns(2)


    with col1:

        if st.button("🟢 Paper Buy"):

            result = paper_trader.buy(
                analyzed_symbol,
                price,
                quantity
            )


            st.success(result)


    with col2:

        if st.button("🔴 Paper Sell"):

            result = paper_trader.sell(
                analyzed_symbol,
                price,
                quantity
            )


            st.warning(result)


    # Virtual Portfolio
    st.header("📦 Virtual Portfolio")


    portfolio_data = (
        paper_trader.get_portfolio_value(
            market
        )
    )


    if portfolio_data["holdings"]:

        st.metric(
            "Portfolio Value",
            f"₹{portfolio_data['total_value']:,.2f}"
        )


        for symbol_name, details in (
            portfolio_data["holdings"].items()
        ):

            st.subheader(symbol_name)


            col1, col2, col3 = st.columns(3)


            col1.metric(
                "Quantity",
                details["quantity"]
            )


            col2.metric(
                "Current Price",
                f"₹{details['current_price']}"
            )


            col3.metric(
                "Profit / Loss",
                f"₹{details['profit_loss']}"
            )


            st.write(
                f"Average Buy Price: "
                f"₹{details['average_price']}"
            )


            st.write(
                f"Return: "
                f"{details['return_percent']}%"
            )


    else:

        st.info(
            "No virtual holdings yet."
        )


    # Trade History
    st.header("📜 Trade History")


    history = (
        paper_trader.get_trade_history()
    )


    if history:

        st.json(history)


    else:

        st.info(
            "No paper trades yet."
        )