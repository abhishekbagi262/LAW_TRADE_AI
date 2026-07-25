from backend.backtesting.backtester import Backtester


# ==============================
# CREATE BACKTESTER
# ==============================

backtester = Backtester(

    starting_balance=100000,

    stop_loss_percent=5,

    take_profit_percent=10,

    position_size_percent=25,

    transaction_cost_percent=0.1,

    slippage_percent=0.05

)


# ==============================
# RUN WALK-FORWARD TEST
# ==============================

result = backtester.run_walk_forward(

    symbol="RELIANCE.NS",

    period="5y",

    train_ratio=0.60

)


# ==============================
# DISPLAY RESULT
# ==============================

print("\n==============================")

print(
    "WALK-FORWARD RESULT"
)

print(
    "=============================="
)


if result:

    print(
        f"Symbol: "
        f"{result['symbol']}"
    )


    print(
        f"Training Period: "
        f"{result['training_start']} "
        f"to "
        f"{result['training_end']}"
    )


    print(
        f"Testing Period: "
        f"{result['testing_start']} "
        f"to "
        f"{result['testing_end']}"
    )


    # ==============================
    # TRAINING PERFORMANCE
    # ==============================

    print(
        "\n=============================="
    )

    print(
        "TRAINING PERFORMANCE"
    )

    print(
        "=============================="
    )


    print(
        f"LAW TRADE AI Strategy Return: "
        f"{result['training_strategy_return']}%"
    )


    print(
        f"Buy & Hold Return: "
        f"{result['training_buy_and_hold_return']}%"
    )


    # ==============================
    # TESTING PERFORMANCE
    # ==============================

    print(
        "\n=============================="
    )

    print(
        "TESTING PERFORMANCE"
    )

    print(
        "=============================="
    )


    print(
        f"LAW TRADE AI Strategy Return: "
        f"{result['testing_strategy_return']}%"
    )


    print(
        f"Buy & Hold Return: "
        f"{result['testing_buy_and_hold_return']}%"
    )


    # ==============================
    # OUT-OF-SAMPLE COMPARISON
    # ==============================

    print(
        "\n=============================="
    )

    print(
        "OUT-OF-SAMPLE COMPARISON"
    )

    print(
        "=============================="
    )


    strategy_return = (

        result['testing_strategy_return']

    )


    buy_and_hold_return = (

        result['testing_buy_and_hold_return']

    )


    difference = (

        strategy_return

        - buy_and_hold_return

    )


    print(
        f"Strategy vs Buy & Hold: "
        f"{round(difference, 2)}%"
    )


    if strategy_return > buy_and_hold_return:

        print(
            "✅ LAW TRADE AI BEAT BUY & HOLD"
        )

    else:

        print(
            "❌ LAW TRADE AI DID NOT BEAT BUY & HOLD"
        )


else:

    print(
        "Walk-forward test failed."
    )