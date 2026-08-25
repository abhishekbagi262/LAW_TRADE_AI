from backend.backtesting.backtester import Backtester


symbols = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ITC.NS"
]


for symbol in symbols:

    backtester = Backtester(
        starting_balance=100000
    )


    result = backtester.run(
        symbol,
        period="5y"
    )


    print("\n==============================")
    print(
        f"BACKTEST RESULT: {symbol}"
    )
    print("==============================")


    if result is not None:

        print(
            f"Starting Balance: "
            f"₹{result['starting_balance']}"
        )

        print(
            f"Final Balance: "
            f"₹{result['final_balance']}"
        )

        print(
            f"Return: "
            f"₹{result['total_return']}"
        )

        print(
            f"Return Percentage: "
            f"{result['return_percent']}%"
        )
        print(
             f"Maximum Drawdown: "
             f"₹{result['maximum_drawdown']}"
        )
        print(
            f"Maximum Drawdown Percentage: "
            f"{result['maximum_drawdown_percent']}%"
        )

        print(
            f"Buy & Hold Return: "
            f"{result['buy_and_hold_return_percent']}%"
        )

        print(
            f"Total Trades: "
            f"{result['total_trades']}"
        )

        print(
            f"Winning Trades: "
            f"{result['winning_trades']}"
        )

        print(
            f"Losing Trades: "
            f"{result['losing_trades']}"
        )
