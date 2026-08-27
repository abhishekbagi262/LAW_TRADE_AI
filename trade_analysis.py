from backend.backtesting.backtester import Backtester
symbols = [

    "RELIANCE.NS",

    "TCS.NS",

    "HDFCBANK.NS",

    "INFY.NS",

    "ITC.NS"

]


print("\n========================================")

print(
    "LAW TRADE AI - TRADE ANALYSIS"
)

print("========================================")


for symbol in symbols:


    print("\n")

    print("==================================================")

    print(
        f"ANALYZING: {symbol}"
    )

    print("==================================================")


    backtester = Backtester(

        starting_balance=100000,

        stop_loss_percent=5,

        take_profit_percent=10,

        position_size_percent=25,

        transaction_cost_percent=0.1,

        slippage_percent=0.05

    )


    result = backtester.run(

        symbol=symbol,

        period="5y"

    )


    if result is None:

        print(
            "No result."
        )

        continue


    trades = result[
        "trades"
    ]


    winning_trades = []

    losing_trades = []


    for trade in trades:


        if "profit_loss" not in trade:

            continue


        profit_loss = trade[
            "profit_loss"
        ]


        if profit_loss > 0:

            winning_trades.append(
                profit_loss
            )


        elif profit_loss < 0:

            losing_trades.append(
                profit_loss
            )


    total_closed_trades = (

        len(winning_trades)

        +

        len(losing_trades)

    )


    if winning_trades:

        average_win = (

            sum(winning_trades)

            /

            len(winning_trades)

        )

        largest_win = max(
            winning_trades
        )

    else:

        average_win = 0

        largest_win = 0


    if losing_trades:

        average_loss = (

            sum(losing_trades)

            /

            len(losing_trades)

        )

        largest_loss = min(
            losing_trades
        )

    else:

        average_loss = 0

        largest_loss = 0


    gross_profit = sum(
        winning_trades
    )


    gross_loss = abs(

        sum(
            losing_trades
        )

    )


    if gross_loss > 0:

        profit_factor = (

            gross_profit

            /

            gross_loss

        )

    else:

        profit_factor = 0


    if total_closed_trades > 0:

        win_rate = (

            len(winning_trades)

            /

            total_closed_trades

        ) * 100

    else:

        win_rate = 0


    print("\n----------------------------------------")

    print(
        "TRADE STATISTICS"
    )

    print("----------------------------------------")


    print(

        f"Total Closed Trades: "
        f"{total_closed_trades}"

    )


    print(

        f"Winning Trades: "
        f"{len(winning_trades)}"

    )


    print(

        f"Losing Trades: "
        f"{len(losing_trades)}"

    )


    print(

        f"Win Rate: "
        f"{round(win_rate, 2)}%"

    )


    print(

        f"Average Winning Trade: "
        f"₹{round(average_win, 2)}"

    )


    print(

        f"Average Losing Trade: "
        f"₹{round(average_loss, 2)}"

    )


    print(

        f"Largest Winning Trade: "
        f"₹{round(largest_win, 2)}"

    )


    print(

        f"Largest Losing Trade: "
        f"₹{round(largest_loss, 2)}"

    )


    print(

        f"Gross Profit: "
        f"₹{round(gross_profit, 2)}"

    )


    print(

        f"Gross Loss: "
        f"₹{round(gross_loss, 2)}"

    )


    print(

        f"Profit Factor: "
        f"{round(profit_factor, 2)}"

    )


    print("\n----------------------------------------")

    print(
        "EXIT REASONS"
    )

    print("----------------------------------------")


    stop_loss_count = 0

    take_profit_count = 0

    signal_count = 0

    final_sell_count = 0


    for trade in trades:


        reason = trade.get(
            "reason",
            ""
        )


        if reason == "STOP LOSS":

            stop_loss_count += 1


        elif reason == "TAKE PROFIT":

            take_profit_count += 1


        elif reason == "SIGNAL":

            signal_count += 1


        elif reason == "END OF BACKTEST":

            final_sell_count += 1


    print(

        f"Stop Loss Exits: "
        f"{stop_loss_count}"

    )


    print(

        f"Take Profit Exits: "
        f"{take_profit_count}"

    )


    print(

        f"Signal Exits: "
        f"{signal_count}"

    )


    print(

        f"End of Backtest Exits: "
        f"{final_sell_count}"

    )


print("\n========================================")

print(
    "TRADE ANALYSIS COMPLETED"
)

print("========================================")
