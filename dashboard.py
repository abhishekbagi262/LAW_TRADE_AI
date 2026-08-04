import streamlit as st
import pandas as pd

from backend.market.market_data import MarketData
from backend.market.technical_analysis import TechnicalAnalysis
from backend.ai.decision_engine import DecisionEngine
from backend.trading.paper_trading import PaperTrading
from backend.risk.risk_manager import RiskManager
from backend import config
from backend.market_scanner import MarketScanner
from backend.stock_analyzer import StockAnalyzer


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


stock_analyzer = StockAnalyzer(
    market,
    technical,
    decision_engine,
    risk_manager,
    config
)
market_scanner = MarketScanner(stock_analyzer)


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

        stock_data = stock_analyzer.analyze_stock(symbol)

    if stock_data is None:

        st.error(
            "Invalid stock symbol or data unavailable."
        )

    else:

        st.session_state.analysis = stock_data

        st.success(
            "Stock analyzed successfully!"
        )
        scanner_data = market_scanner.scan_market()

        st.session_state.scanner_data = scanner_data

# =========================
# AI MARKET SCANNER
# =========================

if "scanner_data" in st.session_state:

    st.header(
        "📈 AI Market Scanner"
    )

    signal_filter = st.selectbox(
        "Signal",
        ["All", "BUY", "HOLD", "AVOID"]
    )

    confidence_filter = st.slider(
        "Minimum Confidence (%)",
        min_value=0,
        max_value=100,
        value=50
    )

    quality_filter = st.slider(
        "Minimum Trade Quality",
        min_value=0,
        max_value=10,
        value=5
    )

    filtered_data = st.session_state.scanner_data

    if signal_filter != "All":
        filtered_data = [

            stock

            for stock in filtered_data

            if stock["Signal"] == signal_filter

        ]

    filtered_data = [

        stock

        for stock in filtered_data

        if float(
            stock["Confidence"].replace("%", "")
        ) >= confidence_filter
    ]
    filtered_data = [
        stock

        for stock in filtered_data

        if int(

            stock["Quality"].split("/")[0]
        ) >= quality_filter
    ]

    st.table(filtered_data)
        
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


    col1, col2, col3, col4 = (
        st.columns(4)
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
    st.subheader("🏆 Trade Quality")

    quality = data["trade_quality"]

    if quality >= 9:
        grade = "A+"
    elif quality >= 8:
        grade = "A"
    elif quality >= 7:
        grade = "B"
    elif quality >= 6:
        grade = "C"
    else:
        grade = "D"

    col1, col2 = st.columns(2)

    col1.metric(
        "Trade Quality",
        f"{quality}/10"
    )

    col2.metric(
        "Grade",
        grade
    )
    if quality >= 9:
        stars = "★★★★★"
    elif quality >= 8:
        stars = "★★★★☆"
    elif quality >= 7:
        stars = "★★★☆☆"
    elif quality >= 6:
        stars = "★★☆☆☆"
    else:
        stars = "★☆☆☆☆"

    st.write(f"### {stars}")
    

    # =========================
    # RISK MANAGEMENT
    # =========================

    st.header("🛡️ Risk Management")
    if data["decision"]["signal"] == "BUY":
        col1, col2, col3, col4, col5, col6 = st.columns(6)

        col1.metric(
            "Entry",
            f"₹{data['entry_price']}"
        )

        col2.metric(
            "Stop Loss",
            f"₹{data['stop_loss']}"
        )

        col3.metric(
            "Target 1",
            f"₹{data['targets']['target1']}"
        )
        col4.metric(
            "Target 2",
            f"₹{data['targets']['target2']}"
        )

        col5.metric(
            "Quantity",
            data["position_size"]
        )

        col6.metric(
            "Risk/Reward",
            f"1 : {data['targets']['rr2']}"
        )
    else:
        st.warning(
            f"""
    🚫 No trade setup generated.

    Current AI Signal: {data['decision']['signal']}

    LAW TRADE AI does not recommend opening a new position
    until the signal changes to BUY.
    """
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


            if result == "Insufficient virtual balance.":
                st.error(result)
            else:
                st.success(result)
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


            col1, col2, col3, col4 = st.columns(4)

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
            # =========================
            # AI Portfolio Advice
            # =========================

            try:
                info = market.get_company_info(symbol_name)
                analysis = market.get_analysis_data(symbol_name)

                technical_data = technical.get_technical_analysis(symbol_name)

                fundamental_data = {
                    "pe_ratio": info.get("trailingPE"),

                    "profit_margin": analysis.get("profit_margin"),

                    "revenue_growth": analysis.get("revenue_growth"),

                    "earnings_growth": analysis.get("earnings_growth")

                }
                portfolio_decision = decision_engine.generate_signal(
                    fundamental_data,
                    technical_data
                )
                signal = portfolio_decision["signal"]
                confidence = portfolio_decision["confidence"]
                if signal == "BUY":

                    st.success(
                        f"🟢 BUY ({confidence}%)"
                    )

                elif signal == "HOLD":
                    st.warning(
                        f"🟡 HOLD ({confidence}%)"
                    )

                else:
                    st.error(
                        f"🔴 AVOID ({confidence}%)"
                )
                
            except Exception:
                st.warning(
                    "AI recommendation unavailable."
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
        history_df = pd.DataFrame(history)
        st.dataframe(
            history_df,
            use_container_width=True
        )


    else:


        st.info(

            "No paper trades yet."

        )

# =========================
# AI STOCK RECOMMENDATION
# =========================

st.header("🤖 AI Stock Recommendation")

recommendation_symbols = st.text_input(
    "Stocks to Analyze",
    "RELIANCE.NS, TCS.NS, HDFCBANK.NS, INFY.NS, ITC.NS",
    key="recommendation_symbols"
)

if st.button("🚀 Find Best Stock"):

    recommendation_results = []

    stocks = [
        stock.strip().upper()
        for stock in recommendation_symbols.split(",")
        if stock.strip()
    ]

    with st.spinner("Analyzing stocks..."):

        for stock in stocks:

            try:

                price = market.get_current_price(stock)

                if price is None:
                    continue

                info = market.get_company_info(stock)
                analysis = market.get_analysis_data(stock)
                technical_data = technical.get_technical_analysis(stock)

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

                stop_loss = risk_manager.calculate_stop_loss(
                    price,
                    technical_data["atr"]
                )
                targets = risk_manager.calculate_targets(
                    entry_price,
                    stop_loss
                )

                quantity = risk_manager.calculate_position_size(
                    config.INITIAL_BALANCE,
                    price,
                    stop_loss
                )

                if (
                    decision["signal"] == "BUY"
                    and decision["score"] >= 8
                ):
                    recommendation_results.append({
                        "Stock": stock,

                        "Signal": decision["signal"],

                        "Score": decision["score"],

                        "Confidence": f"{decision['confidence']}%",

                        "Price": price,

                        "Suggested Qty": quantity
                    })

            except Exception:
                continue

    if recommendation_results:
        recommendation_results.sort(
            key=lambda item: item["Score"],
            reverse=True
        )
        for index, stock in enumerate(recommendation_results, start=1):
            stock["Rank"] = index

        recommendation_df = pd.DataFrame(
            recommendation_results
        )
        recommendation_df = recommendation_df[
            [
                "Rank",
                "Stock",
                "Signal",
                "Score",
                "Confidence",
                "Price",
                "Suggested Qty"
            ]
        ]

        st.subheader("🏆 AI Recommendations")
        st.dataframe(
            recommendation_df,
            use_container_width=True
        )

        best_stock = recommendation_results[0]

        st.success(
            f"🏆 Best AI Pick: {best_stock['Stock']} | "
            f"Signal: {best_stock['Signal']} | "
            f"Score: {best_stock['Score']} | "
            f"Confidence: {best_stock['Confidence']} | "
            f"Suggested Qty: {best_stock['Suggested Qty']}"
        )

    else:
        st.info(
            "📉 No strong BUY opportunities found today.\n\n"
            "All analyzed stocks are either HOLD, AVOID, or have a score below 8."
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

                    col4.metric(
                        "Win Rate",

                        f"{result['performance']['win_rate']}%"
                    )

                    st.subheader(
                        "📊 Advanced Performance Metrics"
                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Profit Factor",
                        result["performance"]["profit_factor"]
                    )

                    col2.metric(
                        "Average Win",
                        f"₹{result['performance']['average_win']}"
                    )
                    col3.metric(

                        "Average Loss",
                        f"₹{abs(result['performance']['average_loss'])}"
                    )
                    col4.metric(
                        "Expectancy",
                        f"₹{result['performance']['expectancy']}"
                    )


                    col1, col2, col3 = st.columns(3)
                    col1.metric(
                        "Largest Win",
                        f"₹{result['performance']['largest_win']}"
                    )
                    col2.metric(
                        "Largest Loss",
                        f"₹{abs(result['performance']['largest_loss'])}"
                    )

                    col3.metric(
                        "Realized P/L",
                        f"₹{result['performance']['total_realized_profit_loss']}"
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