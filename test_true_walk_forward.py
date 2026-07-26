import yfinance as yf

from backend.backtesting.backtester import Backtester


# =========================================
# CONFIGURATION
# =========================================

SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "HDFCBANK.NS",
    "INFY.NS",
    "ITC.NS"
]

PERIOD = "5y"

TRAINING_DAYS = 504      # Approximately 2 years
TESTING_DAYS = 126       # Approximately 6 months
STEP_DAYS = 126          # Move forward 6 months

STARTING_BALANCE = 100000


# =========================================
# TRUE WALK-FORWARD TEST
# =========================================

def run_true_walk_forward(symbol):

    print("\n" + "=" * 60)
    print(f"TRUE WALK-FORWARD TEST: {symbol}")
    print("=" * 60)

    stock = yf.Ticker(symbol)

    data = stock.history(
        period=PERIOD
    )

    if data.empty:

        print("No data found.")

        return

    total_days = len(data)

    results = []

    start_index = 0

    while (

        start_index
        +
        TRAINING_DAYS
        +
        TESTING_DAYS
        <=
        total_days

    ):

        # =========================================
        # SPLIT TRAINING AND TESTING DATA
        # =========================================

        training_start = start_index

        training_end = (

            start_index
            +
            TRAINING_DAYS

        )

        testing_start = training_end

        testing_end = (

            testing_start
            +
            TESTING_DAYS

        )


        training_data = data.iloc[

            training_start:
            training_end

        ]


        testing_data = data.iloc[

            testing_start:
            testing_end

        ]


        print("\n" + "-" * 50)

        print(
            f"TRAINING: "
            f"{training_data.index[0].date()} "
            f"to "
            f"{training_data.index[-1].date()}"
        )

        print(
            f"TESTING: "
            f"{testing_data.index[0].date()} "
            f"to "
            f"{testing_data.index[-1].date()}"
        )


        # =========================================
        # TRAINING PHASE
        # =========================================

        training_backtester = Backtester(

            starting_balance=STARTING_BALANCE,

            stop_loss_percent=5,

            take_profit_percent=10,

            position_size_percent=25,

            transaction_cost_percent=0.1,

            slippage_percent=0.05

        )


        training_result = (

            training_backtester._run_on_data(

                symbol,

                training_data

            )

        )


        # =========================================
        # TESTING PHASE
        # =========================================

        testing_backtester = Backtester(

            starting_balance=STARTING_BALANCE,

            stop_loss_percent=5,

            take_profit_percent=10,

            position_size_percent=25,

            transaction_cost_percent=0.1,

            slippage_percent=0.05

        )


        result = (

            testing_backtester._run_on_data(

                symbol,

                testing_data

            )

        )


        if result is not None:

            results.append(result)

            print(
                f"Testing Return: "
                f"{result['return_percent']}%"
            )

            print(
                f"Buy & Hold Return: "
                f"{result['buy_and_hold_return_percent']}%"
            )

            print(
                f"Trades: "
                f"{result['total_trades']}"
            )


        # =========================================
        # MOVE WINDOW FORWARD
        # =========================================

        start_index += STEP_DAYS


    # =========================================
    # FINAL RESULTS
    # =========================================

    print("\n" + "=" * 60)

    print(
        f"COMPLETED WALK-FORWARD TEST: {symbol}"
    )

    print("=" * 60)

    print(
        f"Number of testing windows: "
        f"{len(results)}"
    )


    if results:

        total_strategy_return = sum(

            result["return_percent"]

            for result in results

        )


        total_buy_hold_return = sum(

            result["buy_and_hold_return_percent"]

            for result in results

        )


        print(

            f"Total Strategy Return: "
            f"{round(total_strategy_return, 2)}%"

        )


        print(

            f"Total Buy & Hold Return: "
            f"{round(total_buy_hold_return, 2)}%"

        )


    return results


# =========================================
# RUN ALL SYMBOLS
# =========================================

for symbol in SYMBOLS:

    run_true_walk_forward(symbol)