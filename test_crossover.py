from backend.backtesting.crossover_backtester import (
    CrossoverBacktester
)


symbols = [

    "RELIANCE.NS",

    "TCS.NS",

    "HDFCBANK.NS",

    "INFY.NS",

    "ITC.NS"

]


for symbol in symbols:


    backtester = (

        CrossoverBacktester(

            starting_balance=100000

        )

    )


    result = (

        backtester.run(

            symbol,

            period="3y"

        )

    )


    print(

        "\n=============================="

    )


    print(

        f"CROSSOVER BACKTEST: "

        f"{symbol}"

    )


    print(

        "=============================="

    )


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