from backend.backtesting.backtester import Backtester


symbols = [

    "RELIANCE.NS",

    "TCS.NS",

    "HDFCBANK.NS",

    "INFY.NS",

    "ITC.NS"

]


starting_balance = 100000


capital_per_stock = (

    starting_balance
    /
    len(symbols)

)


print("\n========================================")
print("LAW TRADE AI - PORTFOLIO BACKTEST")
print("========================================")


print(
    f"\nTotal Portfolio: ₹{starting_balance}"
)


print(
    f"Capital Per Stock: ₹{capital_per_stock}"
)


total_strategy_return = 0


total_buy_hold_return = 0


results = []


for symbol in symbols:


    print("\n")
    print("=" * 50)

    print(
        f"TESTING: {symbol}"
    )

    print("=" * 50)


    backtester = Backtester(

        starting_balance=capital_per_stock,

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
            f"Skipping {symbol}"
        )

        continue


    strategy_return = (

        result[
            "testing_strategy_return"
        ]

    )


    buy_hold_return = (

        result[
            "testing_buy_and_hold_return"
        ]

    )


    total_strategy_return += (

        strategy_return

    )


    total_buy_hold_return += (

        buy_hold_return

    )


    results.append({

        "symbol": symbol,

        "strategy_return":
            strategy_return,

        "buy_hold_return":
            buy_hold_return

    })


# ========================================
# PORTFOLIO PERFORMANCE
# ========================================


portfolio_strategy_return = (

    total_strategy_return
    /
    len(results)

)


portfolio_buy_hold_return = (

    total_buy_hold_return
    /
    len(results)

)


outperformance = (

    portfolio_strategy_return

    -

    portfolio_buy_hold_return

)


strategy_final_balance = (

    starting_balance

    *

    (

        1

        +

        portfolio_strategy_return
        /
        100

    )

)


buy_hold_final_balance = (

    starting_balance

    *

    (

        1

        +

        portfolio_buy_hold_return
        /
        100

    )

)


print("\n")


print("=" * 50)

print(
    "PORTFOLIO FINAL RESULT"
)

print("=" * 50)


print(

    f"\nStarting Portfolio: "
    f"₹{starting_balance}"

)


print(

    f"LAW TRADE AI Return: "
    f"{round(portfolio_strategy_return, 2)}%"

)


print(

    f"LAW TRADE AI Final Balance: "
    f"₹{round(strategy_final_balance, 2)}"

)


print(

    f"\nBuy & Hold Return: "
    f"{round(portfolio_buy_hold_return, 2)}%"

)


print(

    f"Buy & Hold Final Balance: "
    f"₹{round(buy_hold_final_balance, 2)}"

)


print(

    f"\nOutperformance: "
    f"{round(outperformance, 2)}%"

)


if outperformance > 0:

    print(
        "\n✅ LAW TRADE AI BEAT BUY & HOLD"
    )

else:

    print(
        "\n❌ LAW TRADE AI UNDERPERFORMED"
    )


print("\n")


print("=" * 50)

print(
    "PORTFOLIO STOCK BREAKDOWN"
)

print("=" * 50)


for result in results:


    print(

        f"\n{result['symbol']}"

    )


    print(

        f"Strategy: "
        f"{result['strategy_return']}%"

    )


    print(

        f"Buy & Hold: "
        f"{result['buy_hold_return']}%"

    )


print("\n")


print("=" * 50)

print(
    "PORTFOLIO BACKTEST COMPLETED"
)

print("=" * 50)