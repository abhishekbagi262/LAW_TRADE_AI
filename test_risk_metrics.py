import yfinance as yf
import numpy as np

from backend.backtesting.backtester import Backtester


# =========================================================
# CONFIGURATION
# =========================================================

symbols = [

    "RELIANCE.NS",

    "TCS.NS",

    "HDFCBANK.NS",

    "INFY.NS",

    "ITC.NS"

]


starting_balance = 100000


train_ratio = 0.60


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def calculate_sharpe_ratio(
    returns
):

    returns = np.array(
        returns
    )

    if len(returns) < 2:

        return 0

    average_return = np.mean(
        returns
    )

    standard_deviation = np.std(
        returns
    )

    if standard_deviation == 0:

        return 0

    return (

        average_return
        /
        standard_deviation

    ) * np.sqrt(252)


def calculate_maximum_drawdown(
    equity_curve
):

    if not equity_curve:

        return 0

    equity_curve = np.array(
        equity_curve
    )

    running_maximum = np.maximum.accumulate(
        equity_curve
    )

    drawdowns = (

        running_maximum
        -
        equity_curve

    )

    maximum_drawdown = np.max(
        drawdowns
    )

    return maximum_drawdown


def calculate_profit_factor(
    trades
):

    gross_profit = 0

    gross_loss = 0


    for trade in trades:

        if "profit_loss" not in trade:

            continue


        profit_loss = (

            trade[
                "profit_loss"
            ]

        )


        if profit_loss > 0:

            gross_profit += profit_loss


        elif profit_loss < 0:

            gross_loss += abs(
                profit_loss
            )


    if gross_loss == 0:

        return 0


    return (

        gross_profit
        /
        gross_loss

    )


def calculate_win_rate(
    trades
):

    winning_trades = 0

    losing_trades = 0


    for trade in trades:

        if "profit_loss" not in trade:

            continue


        profit_loss = (

            trade[
                "profit_loss"
            ]

        )


        if profit_loss > 0:

            winning_trades += 1


        elif profit_loss < 0:

            losing_trades += 1


    total_trades = (

        winning_trades
        +
        losing_trades

    )


    if total_trades == 0:

        return 0


    return (

        winning_trades
        /
        total_trades

    ) * 100


# =========================================================
# RUN STRATEGY TESTS
# =========================================================

strategy_returns = []


buy_hold_returns = []


all_trades = []


all_equity_curves = []


print("\n========================================")

print(
    "LAW TRADE AI - RISK ANALYSIS"
)

print("========================================")


for symbol in symbols:


    print("\n")

    print(
        f"Testing {symbol}..."
    )


    backtester = Backtester(

        starting_balance=(

            starting_balance
            /
            len(symbols)

        ),

        stop_loss_percent=5,

        take_profit_percent=10,

        position_size_percent=25,

        transaction_cost_percent=0.1,

        slippage_percent=0.05

    )


    result = backtester.run_walk_forward(

        symbol=symbol,

        period="5y",

        train_ratio=train_ratio

    )


    if result is None:

        continue


    strategy_returns.append(

        result[
            "testing_strategy_return"
        ]

    )


    buy_hold_returns.append(

        result[
            "testing_buy_and_hold_return"
        ]

    )


    # Run testing period again
    # to collect trades and equity


    stock = yf.Ticker(
        symbol
    )


    data = stock.history(
        period="5y"
    )


    split_index = int(

        len(data)
        *
        train_ratio

    )


    testing_data = data.iloc[
        split_index:
    ]


    testing_backtester = Backtester(

        starting_balance=(

            starting_balance
            /
            len(symbols)

        ),

        stop_loss_percent=5,

        take_profit_percent=10,

        position_size_percent=25,

        transaction_cost_percent=0.1,

        slippage_percent=0.05

    )


    testing_result = (

        testing_backtester._run_on_data(

            symbol,

            testing_data

        )

    )


    if testing_result is not None:


        all_trades.extend(

            testing_result[
                "trades"
            ]

        )


        all_equity_curves.append(

            testing_result[
                "equity_curve"
            ]

        )


# =========================================================
# PORTFOLIO RETURNS
# =========================================================

portfolio_strategy_return = (

    np.mean(

        strategy_returns

    )

)


portfolio_buy_hold_return = (

    np.mean(

        buy_hold_returns

    )

)


# =========================================================
# NIFTY 50 BENCHMARK
# =========================================================

print("\n")

print(
    "Downloading NIFTY 50 data..."
)


nifty = yf.Ticker(

    "^NSEI"

)


nifty_data = nifty.history(

    period="5y"

)


nifty_split_index = int(

    len(nifty_data)
    *
    train_ratio

)


nifty_testing_data = (

    nifty_data.iloc[
        nifty_split_index:
    ]

)


nifty_start_price = float(

    nifty_testing_data.iloc[0][
        "Close"
    ]

)


nifty_end_price = float(

    nifty_testing_data.iloc[-1][
        "Close"
    ]

)


nifty_return = (

    (

        nifty_end_price
        -
        nifty_start_price

    )

    /

    nifty_start_price

) * 100


# =========================================================
# RISK METRICS
# =========================================================

maximum_drawdown = 0


if all_equity_curves:


    combined_equity_curve = []


    minimum_length = min(

        len(curve)

        for curve in all_equity_curves

    )


    for i in range(
        minimum_length
    ):


        daily_total = sum(

            curve[i]

            for curve in all_equity_curves

        )


        combined_equity_curve.append(

            daily_total

        )


    maximum_drawdown = (

        calculate_maximum_drawdown(

            combined_equity_curve

        )

    )


# Calculate return series

daily_returns = []


if all_equity_curves:


    for i in range(

        1,

        minimum_length

    ):


        previous_value = sum(

            curve[i - 1]

            for curve in all_equity_curves

        )


        current_value = sum(

            curve[i]

            for curve in all_equity_curves

        )


        if previous_value != 0:


            daily_return = (

                (

                    current_value
                    -
                    previous_value

                )

                /

                previous_value

            )


            daily_returns.append(

                daily_return

            )


sharpe_ratio = (

    calculate_sharpe_ratio(

        daily_returns

    )

)


profit_factor = (

    calculate_profit_factor(

        all_trades

    )

)


win_rate = (

    calculate_win_rate(

        all_trades

    )

)


# =========================================================
# FINAL REPORT
# =========================================================

print("\n========================================")

print(
    "FINAL PROFESSIONAL RISK REPORT"
)

print("========================================")


print(

    f"\nLAW TRADE AI Return: "
    f"{round(portfolio_strategy_return, 2)}%"

)


print(

    f"Equal-Weight Buy & Hold: "
    f"{round(portfolio_buy_hold_return, 2)}%"

)


print(

    f"NIFTY 50 Return: "
    f"{round(nifty_return, 2)}%"

)


print(

    f"\nMaximum Drawdown: "
    f"₹{round(maximum_drawdown, 2)}"

)


print(

    f"Sharpe Ratio: "
    f"{round(sharpe_ratio, 2)}"

)


print(

    f"Profit Factor: "
    f"{round(profit_factor, 2)}"

)


print(

    f"Win Rate: "
    f"{round(win_rate, 2)}%"

)


print("\n========================================")

print(
    "RISK ANALYSIS COMPLETED"
)

print("========================================")