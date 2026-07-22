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


market = MarketData()
technical = TechnicalAnalysis()
decision_engine = DecisionEngine()


if "paper_trader" not in st.session_state:
    st.session_state.paper_trader = PaperTrading(
        starting_balance=100000
    )


if "analysis" not in st.session_state:
    st.session_state.analysis = None


paper_trader = st.session_state.paper_trader


st.title("📈 LAW TRADE AI")
st.subheader("AI-Powered Stock Analysis System")


symbol = st.text_input(
    "Enter Stock Symbol",
    "RELIANCE.NS"
).upper()


if st.button("Analyze Stock"):

    with st.spinner("Analyzing stock..."):

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

        st.session_state.analysis = {
            "symbol": symbol,
            "price": price,
            "change": change,
            "info": info,
            "analysis": analysis,
            "technical": technical_data,
            "decision": decision
        }


if st.session_state.analysis is not None:

    data = st.session_state.analysis

    symbol = data["symbol"]
    price = data["price"]
    change = data["change"]
    info = data["info"]
    analysis = data["analysis"]
    technical_data = data["technical"]
    decision = data["decision"]


    if price is not None:

        st.success(
            f"{info.get('longName', 'N/A')} analyzed successfully"
        )


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


        st.header("📈 Price Chart")

        chart_data = market.get_stock_data(
            symbol,
            period="6mo"
        )

        if not chart_data.empty:

            chart_data = chart_data[["Close"]].copy()

            chart_data.index = chart_data.index.tz_localize(None)

            st.line_chart(chart_data)


        st.header("📊 Fundamental Analysis")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Profit Margin",
            analysis.get("profit_margin", "N/A")
        )

        col2.metric(
            "Revenue Growth",
            analysis.get("revenue_growth", "N/A")
        )

        col3.metric(
            "Earnings Growth",
            analysis.get("earnings_growth", "N/A")
        )


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


        st.header("🤖 LAW TRADE AI Decision")

        st.metric(
            "Final Signal",
            decision["signal"]
        )

        st.write(
            f"### Score: {decision['score']}"
        )


        st.subheader("🧠 AI Analysis")

        st.info(
            decision["explanation"]
        )


        st.subheader("AI Reasoning")

        for reason in decision["reasons"]:

            st.write(
                f"• {reason}"
            )


        st.header("💰 Paper Trading")

        st.metric(
            "Available Virtual Balance",
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
                    symbol,
                    price,
                    quantity
                )

                st.success(result)


        with col2:

            if st.button("🔴 Paper Sell"):

                result = paper_trader.sell(
                    symbol,
                    price,
                    quantity
                )

                st.warning(result)


        st.subheader("📦 Virtual Portfolio")

        portfolio = paper_trader.get_portfolio()

        if portfolio:

            st.json(portfolio)

        else:

            st.info(
                "No virtual holdings yet."
            )


        st.subheader("📜 Trade History")

        history = paper_trader.get_trade_history()

        if history:

            st.json(history)

        else:

            st.info(
                "No paper trades yet."
            )


    else:

        st.error(
            "Invalid stock symbol or data unavailable."
        )


else:

    st.info(
        "Enter a stock symbol and click Analyze Stock to begin."
    )