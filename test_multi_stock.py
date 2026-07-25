from backend.backtesting.backtester import Backtester


symbols = [

    "RELIANCE.NS",

    "TCS.NS",

    "HDFCBANK.NS",

    "INFY.NS",

    "ITC.NS"

]


print("\n========================================")
print("LAW TRADE AI - MULTI STOCK TEST")
print("========================================")


for symbol in symbols:

    print("\n")
    print("=" * 50)
    print(f"TESTING: {symbol}")
    print("=" * 50)


    backtester = Backtester(

        starting_balance=100000,

        stop_loss_percent=5,

        take_profit_percent=10,

        position_size_percent=25,

        transaction_cost_percent=0.1,

        slippage_percent=0.05

    )


    result = backtester.run_walk_forward(

        symbol=symbol,

        period="5y",

        train_ratio=0.60

    )


    if result is None:

        print(
            f"Could not test {symbol}"
        )

        continue


    print("\n")
    print("----------------------------------------")
    print("FINAL COMPARISON")
    print("----------------------------------------")


    print(

        f"Training Strategy: "
        f"{result['training_strategy_return']}%"

    )


    print(

        f"Training Buy & Hold: "
        f"{result['training_buy_and_hold_return']}%"

    )


    print(

        f"Testing Strategy: "
        f"{result['testing_strategy_return']}%"

    )


    print(

        f"Testing Buy & Hold: "
        f"{result['testing_buy_and_hold_return']}%"

    )


    outperformance = (

        result["testing_strategy_return"]

        -

        result["testing_buy_and_hold_return"]

    )


    print(

        f"Testing Outperformance: "
        f"{round(outperformance, 2)}%"

    )


    if outperformance > 0:

        print(
            "✅ Strategy Beat Buy & Hold"
        )

    else:

        print(
            "❌ Strategy Underperformed Buy & Hold"
        )


print("\n")
print("========================================")
print("MULTI-STOCK TEST COMPLETED")
print("========================================")