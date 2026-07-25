from backend.backtesting.performance_metrics import (
    PerformanceMetrics
)


trades = [

    {
        "type": "SELL",
        "symbol": "RELIANCE.NS",
        "profit_loss": 461.96
    },

    {
        "type": "SELL",
        "symbol": "INFY.NS",
        "profit_loss": -167.97
    },

    {
        "type": "SELL",
        "symbol": "ITC.NS",
        "profit_loss": -536.34
    },

    {
        "type": "SELL",
        "symbol": "TCS.NS",
        "profit_loss": 173.47
    },

    {
        "type": "SELL",
        "symbol": "ITC.NS",
        "profit_loss": -311.61
    },

    {
        "type": "SELL",
        "symbol": "RELIANCE.NS",
        "profit_loss": -779.60
    },

    {
        "type": "SELL",
        "symbol": "HDFCBANK.NS",
        "profit_loss": 742.80
    }

]


metrics = PerformanceMetrics()


result = metrics.calculate(
    trades
)


print("\n")
print("=" * 40)
print("LAW TRADE AI PERFORMANCE METRICS")
print("=" * 40)

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

print(
    f"Win Rate: "
    f"{result['win_rate']}%"
)

print(
    f"Average Win: "
    f"₹{result['average_win']}"
)

print(
    f"Average Loss: "
    f"₹{result['average_loss']}"
)

print(
    f"Largest Win: "
    f"₹{result['largest_win']}"
)

print(
    f"Largest Loss: "
    f"₹{result['largest_loss']}"
)

print(
    f"Profit Factor: "
    f"{result['profit_factor']}"
)

print(
    f"Total Realized P/L: "
    f"₹{result['total_realized_profit_loss']}"
)