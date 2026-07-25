from backend.backtesting.portfolio_backtester import (
    PortfolioBacktester
)


symbols = [

    "RELIANCE.NS",

    "TCS.NS",

    "HDFCBANK.NS",

    "INFY.NS",

    "ITC.NS"

]


backtester = PortfolioBacktester(

    starting_balance=100000,

    stop_loss_percent=5,

    take_profit_percent=10,

    position_size_percent=20

)


result = backtester.run(

    symbols=symbols,

    period="1y"

)


print("\n")
print("=" * 40)
print("LAW TRADE AI PORTFOLIO BACKTEST")
print("=" * 40)

print(
    f"Starting Balance: "
    f"₹{result['starting_balance']}"
)

print(
    f"Final Balance: "
    f"₹{result['final_balance']}"
)

print(
    f"Total Return: "
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

print("\nTrade History:")

for trade in result["trades"]:

    print(trade)