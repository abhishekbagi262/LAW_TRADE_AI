import streamlit as st

from backend.market.market_data import MarketData
from backend.market.technical_analysis import TechnicalAnalysis
from backend.ai.decision_engine import DecisionEngine


st.set_page_config(
    page_title="LAW TRADE AI",
    page_icon="📈",
    layout="wide"
)


market = MarketData()
technical = TechnicalAnalysis()
decision_engine = DecisionEngine()


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


    if price:

        st.success(
            f"{info.get('longName', 'N/A')} analyzed successfully"
        )

        st.header("📌 Stock Overview")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Price", f"₹{price}")
        col2.metric("Day Change", f"{change}%")
        col3.metric("P/E Ratio", info.get("trailingPE", "N/A"))
        col4.metric("EPS", f"₹{info.get('trailingEps', 'N/A')}")


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


        st.subheader("AI Reasoning")

        for reason in decision["reasons"]:

            st.write(
                f"• {reason}"
            )


    else:

        st.error(
            "Invalid stock symbol or data unavailable."
        )