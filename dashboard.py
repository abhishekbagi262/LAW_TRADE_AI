import streamlit as st
import pandas as pd

from backend.market.market_data import MarketData
from backend.market.technical_analysis import TechnicalAnalysis
from backend.ai.decision_engine import DecisionEngine
from backend.trading.paper_trading import PaperTrading
from backend.risk.risk_manager import RiskManager
from backend import config


# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="LAW TRADE AI",
    page_icon="📈",
    layout="wide"
)


# =========================
# INITIALIZE BACKEND
# =========================

market = MarketData()

technical = TechnicalAnalysis()

decision_engine = DecisionEngine()

risk_manager = RiskManager()
print(risk_manager.__class__.__module__)


# =========================
# PAPER TRADER
# =========================

if "paper_trader" not in st.session_state:

    st.session_state.paper_trader = PaperTrading(
        starting_balance=100000
    )


paper_trader = (
    st.session_state.paper_trader
)


# =========================
# ANALYSIS STATE
# =========================

if "analysis" not in st.session_state:

    st.session_state.analysis = None


# =========================
# TITLE
# =========================

st.title(
    "📈 LAW TRADE AI"
)

st.subheader(
    "AI-Powered Stock Analysis System"
)


# =========================
# SIDEBAR
# =========================

st.sidebar.title(
    "⚙️ LAW TRADE AI"
)

st.sidebar.info(
    "Analyze stocks using market data, "
    "technical indicators, fundamentals "
    "and AI-based decision scoring."
)


# =========================
# STOCK INPUT
# =========================

symbol = st.text_input(
    "Enter Stock Symbol",
    "RELIANCE.NS"
).upper()


# =========================
# ANALYZE STOCK
# =========================

if st.button(
    "🔍 Analyze Stock"
):

    with st.spinner(
        "Analyzing stock..."
    ):

        price = (
            market.get_current_price(
                symbol
            )
        )

        change = (
            market.get_day_change(
                symbol
            )
        )

        info = (
            market.get_company_info(
                symbol
            )
        )

        analysis = (
            market.get_analysis_data(
                symbol
            )
        )

        technical_data = (
            technical.get_technical_analysis(
                symbol
            )
        )


    if price is not None:

        fundamental_data = {

            "pe_ratio": info.get(
                "trailingPE"
            ),

            "profit_margin": analysis.get(
                "profit_margin"
            ),

            "revenue_growth": analysis.get(
                "revenue_growth"
            ),

            "earnings_growth": analysis.get(
                "earnings_growth"
            )

        }


        decision = (
            decision_engine.generate_signal(
                fundamental_data,
                technical_data
            )
        )
        entry_price = price

        stop_loss = risk_manager.calculate_stop_loss(
            entry_price,
            technical_data["atr"]
        )

        position_size = risk_manager.calculate_position_size(
            config.INITIAL_BALANCE,
            entry_price,
            stop_loss
        )


        st.session_state.analysis = {

            "symbol": symbol,

            "price": price,

            "change": change,

            "info": info,

            "analysis": analysis,

            "technical_data": technical_data,

            "decision": decision,

            "entry_price": entry_price,

            "stop_loss": stop_loss,

            "position_size": position_size

        }


        st.success(
            "Stock analyzed successfully!"
        )


    else:

        st.error(
            "Invalid stock symbol or "
            "data unavailable."
        )


# =========================
# DISPLAY ANALYSIS
# =========================

if (
    st.session_state.analysis
    is not None
):


    data = (
        st.session_state.analysis
    )


    analyzed_symbol = (
        data["symbol"]
    )


    price = (
        data["price"]
    )


    change = (
        data["change"]
    )


    info = (
        data["info"]
    )


    analysis = (
        data["analysis"]
    )


    technical_data = (
        data["technical_data"]
    )


    decision = (
        data["decision"]
    )


    # =========================
    # SUCCESS MESSAGE
    # =========================

    st.success(

        f"{info.get('longName', 'N/A')} "
        "analyzed successfully"

    )


    # =========================
    # STOCK OVERVIEW
    # =========================

    st.header(
        "📌 Stock Overview"
    )


    col1, col2, col3, col4 = (
        st.columns(4)
    )


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

        info.get(

            "trailingPE",

            "N/A"

        )

    )


    col4.metric(

        "EPS",

        f"₹{info.get('trailingEps', 'N/A')}"

    )


    # =========================
    # PRICE CHART
    # =========================

    st.header(
        "📈 Price Chart"
    )


    chart_data = (
        market.get_stock_data(
            analyzed_symbol,
            period="6mo"
        )
    )


    if not chart_data.empty:


        chart_data = (
            chart_data[
                ["Close"]
            ].copy()
        )


        if (
            chart_data.index.tz
            is not None
        ):

            chart_data.index = (
                chart_data.index.tz_localize(
                    None
                )
            )


        st.line_chart(
            chart_data
        )


    # =========================
    # FUNDAMENTAL ANALYSIS
    # =========================

    st.header(
        "📊 Fundamental Analysis"
    )


    col1, col2, col3 = (
        st.columns(3)
    )


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


    # =========================
    # TECHNICAL ANALYSIS
    # =========================

    st.header(
        "📈 Technical Analysis"
    )


    if technical_data:


        col1, col2, col3, col4 = (
            st.columns(4)
        )


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


    # =========================
    # AI DECISION
    # =========================

    st.header(
        "🤖 LAW TRADE AI Decision"
    )


    st.metric(

        "Final Signal",

        decision["signal"]

    )


    st.write(
        f"### Score: {decision['score']}"
    )

    st.write(
        f"### Confidence: {decision['confidence']}%"
        )


    st.subheader(
        "AI Reasoning"
    )


    for reason in (
        decision["reasons"]
    ):

        st.write(
            f"• {reason}"
        )

    # =========================
    # RISK MANAGEMENT
    # =========================

    st.header("🛡️ Risk Management")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Entry Price",
        f"₹{data['entry_price']}"
    )

    col2.metric(
        "Stop Loss",
        f"₹{data['stop_loss']}"
    )

    col3.metric(
        "Recommended Quantity",
        data["position_size"]
    )


    # =========================
    # PAPER TRADING
    # =========================

    st.header(
        "💰 Paper Trading"
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


    col1, col2 = (
        st.columns(2)
    )


    # =========================
    # PAPER BUY
    # =========================

    with col1:


        if st.button(
            "🟢 Paper Buy"
        ):


            result = (
                paper_trader.buy(

                    analyzed_symbol,

                    price,

                    quantity

                )
            )


            st.success(
                result
            )


            st.rerun()


    # =========================
    # PAPER SELL
    # =========================

    with col2:


        if st.button(
            "🔴 Paper Sell"
        ):


            result = (
                paper_trader.sell(

                    analyzed_symbol,

                    price,

                    quantity

                )
            )


            st.warning(
                result
            )


            st.rerun()


    # =========================
    # VIRTUAL PORTFOLIO
    # =========================

    st.header(
        "📦 Virtual Portfolio"
    )


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


        for (

            symbol_name,

            details

        ) in (

            portfolio_data[

                "holdings"

            ].items()

        ):


            st.subheader(

                symbol_name

            )


            col1, col2, col3 = (
                st.columns(3)
            )


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

                "Average Buy Price: "

                f"₹{details['average_price']}"

            )


            st.write(

                "Return: "

                f"{details['return_percent']}%"

            )


    else:


        st.info(

            "No virtual holdings yet."

        )


    # =========================
    # TRADE HISTORY
    # =========================

    st.header(
        "📜 Trade History"
    )


    history = (

        paper_trader.get_trade_history()

    )


    if history:


        st.json(

            history

        )


    else:


        st.info(

            "No paper trades yet."

        )


# ============================================================
# STOCK COMPARISON SECTION
# ============================================================

st.divider()


st.header(
    "📊 Stock Comparison"
)


st.write(

    "Compare multiple stocks using "

    "return, drawdown, win rate and "

    "overall score."

)


comparison_symbols = st.text_input(

    "Enter stocks separated by commas",

    "RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS, ITC.NS"

)


if st.button(

    "🏆 Compare Stocks"

):


    comparison_results = []


    stocks = [

        stock.strip().upper()

        for stock in (

            comparison_symbols.split(",")

        )

        if stock.strip()

    ]


    with st.spinner(

        "Comparing stocks..."

    ):


        for stock_symbol in stocks:


            try:


                result = (

                    market.get_stock_comparison_data(

                        stock_symbol

                    )

                )


                if result is None:

                    continue


                total_trades = (

                    result.get(

                        "total_trades",

                        0

                    )

                )


                winning_trades = (

                    result.get(

                        "winning_trades",

                        0

                    )

                )


                if total_trades > 0:


                    win_rate = (

                        winning_trades

                        / total_trades

                    ) * 100


                else:


                    win_rate = 0


                return_percent = (

                    result.get(

                        "return_percent",

                        0

                    )

                )


                drawdown_percent = (

                    result.get(

                        "maximum_drawdown_percent",

                        0

                    )

                )


                # =========================
                # OVERALL SCORE
                # =========================

                score = (

                    return_percent * 0.5

                    + win_rate * 0.3

                    - drawdown_percent * 0.2

                )


                comparison_results.append({

                    "Stock": stock_symbol,

                    "Return %": round(

                        return_percent,

                        2

                    ),

                    "Max Drawdown %": round(

                        drawdown_percent,

                        2

                    ),

                    "Win Rate %": round(

                        win_rate,

                        2

                    ),

                    "Overall Score": round(

                        score,

                        2

                    )

                })


            except Exception as error:


                st.warning(

                    f"Could not analyze "

                    f"{stock_symbol}: "

                    f"{error}"

                )


    # =========================
    # DISPLAY COMPARISON
    # =========================

    if comparison_results:


        comparison_results.sort(

            key=lambda item:

            item["Overall Score"],

            reverse=True

        )


        for index, result in enumerate(

            comparison_results,

            start=1

        ):


            result["Rank"] = index


        st.success(

            "Stock ranking completed!"

        )


        comparison_df = pd.DataFrame(

            comparison_results

        )


        st.dataframe(

            comparison_df,

            use_container_width=True

        )


        # =========================
        # RETURN COMPARISON
        # =========================

        st.subheader(

            "📊 Return Comparison"

        )


        return_chart = (

            comparison_df.set_index(

                "Stock"

            )[

                [

                    "Return %"

                ]

            ]

        )


        st.bar_chart(

            return_chart

        )


        # =========================
        # SCORE COMPARISON
        # =========================

        st.subheader(

            "🏆 Overall Score Comparison"

        )


        score_chart = (

            comparison_df.set_index(

                "Stock"

            )[

                [

                    "Overall Score"

                ]

            ]

        )


        st.bar_chart(

            score_chart

        )


        # =========================
        # DRAWDOWN COMPARISON
        # =========================

        st.subheader(

            "📉 Maximum Drawdown Comparison"

        )


        drawdown_chart = (

            comparison_df.set_index(

                "Stock"

            )[

                [

                    "Max Drawdown %"

                ]

            ]

        )


        st.bar_chart(

            drawdown_chart

        )


        # =========================
        # BEST STOCK
        # =========================

        best_stock = (

            comparison_results[0]

        )


        st.subheader(

            "🏆 Best Performing Stock"

        )


        st.success(

            f"🏆 {best_stock['Stock']} "

            f"ranked #1 with an "

            f"Overall Score of "

            f"{best_stock['Overall Score']}"

        )


    else:


        st.info(

            "Enter valid stock symbols "

            "and compare them."

        )
# =========================
# PORTFOLIO BACKTEST
# =========================

st.header(
    "💼 Portfolio Backtest"
)

st.write(
    "Test multiple stocks together "
    "using historical data."
)


portfolio_symbols = st.text_input(

    "Enter portfolio stocks "
    "(comma-separated)",

    "RELIANCE.NS, TCS.NS, "
    "HDFCBANK.NS, INFY.NS, ITC.NS",

    key="portfolio_symbols"

)


portfolio_balance = st.number_input(

    "Starting Portfolio Balance",

    min_value=1000,

    value=100000,

    step=1000,

    key="portfolio_balance"

)


if st.button(
    "🚀 Run Portfolio Backtest"
):

    symbols = [

        symbol.strip().upper()

        for symbol in
        portfolio_symbols.split(",")

        if symbol.strip()

    ]


    if not symbols:

        st.error(
            "Please enter valid stock symbols."
        )

    else:

        with st.spinner(
            "Running portfolio backtest..."
        ):

            try:

                from backend.backtesting.portfolio_backtester import (
                    PortfolioBacktester
                )


                portfolio_backtester = (

                    PortfolioBacktester(

                        starting_balance=
                        portfolio_balance

                    )

                )


                result = (

                    portfolio_backtester.run(

                        symbols

                    )

                )


                if result is None:

                    st.error(

                        "Portfolio backtest failed."

                    )

                else:

                    st.success(

                        "Portfolio backtest completed!"

                    )


                    st.subheader(

                        "📊 Portfolio Performance"

                    )


                    col1, col2, col3, col4 = (

                        st.columns(4)

                    )


                    col1.metric(

                        "Starting Balance",

                        f"₹{result['starting_balance']:,.2f}"

                    )


                    col2.metric(

                        "Final Balance",

                        f"₹{result['final_balance']:,.2f}"

                    )


                    col3.metric(

                        "Total Return",

                        f"₹{result['total_return']:,.2f}"

                    )


                    col4.metric(

                        "Return %",

                        f"{result['return_percent']}%"

                    )


                    st.subheader(

                        "📉 Risk Metrics"

                    )


                    col1, col2 = (

                        st.columns(2)

                    )


                    col1.metric(

                        "Maximum Drawdown",

                        f"₹{result['maximum_drawdown']:,.2f}"

                    )


                    col2.metric(

                        "Maximum Drawdown %",

                        f"{result['maximum_drawdown_percent']}%"

                    )


                    st.subheader(

                        "📈 Trade Statistics"

                    )


                    col1, col2, col3 = (

                        st.columns(3)

                    )


                    col1.metric(

                        "Total Trades",

                        result["total_trades"]

                    )


                    col2.metric(

                        "Winning Trades",

                        result["winning_trades"]

                    )


                    col3.metric(

                        "Losing Trades",

                        result["losing_trades"]

                    )


                    st.subheader(

                        "📜 Portfolio Trade History"

                    )


                    if result["trades"]:

                        st.dataframe(

                            result["trades"],

                            use_container_width=True

                        )

                    else:

                        st.info(

                            "No trades generated."

                        )


            except Exception as error:

                st.error(

                    f"Portfolio backtest error: "

                    f"{error}"

                )