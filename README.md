# LAW TRADER AI

LAW TRADER AI is a Python-based stock-trading research and backtesting system focused on testing technical-analysis strategies on Indian equities.

The project currently evaluates:

- SMA 20 / SMA 50 trend crossovers
- RSI
- MACD
- ATR-based risk management
- Stop loss
- Take profit
- Trailing stop
- Transaction costs
- Slippage
- Rolling walk-forward testing
- Out-of-sample analysis
- Entry-condition analysis
- Exposure analysis
- Strategy-variant comparison
- Exit-variant comparison
- Buy-and-hold benchmarking

The goal of the project is not simply to maximize historical returns, but to determine whether a strategy remains useful when tested on unseen data.

---

## Project Status

**Research / Backtesting Stage**

The system is currently undergoing strategy validation and is **not presented as a proven profitable trading system**.

The research process currently emphasizes:

1. avoiding look-ahead bias
2. realistic next-day execution
3. transaction costs and slippage
4. rolling out-of-sample testing
5. comparison against passive benchmarks
6. avoiding excessive parameter optimization
7. testing entry and exit variations independently

---

# Strategy

The current production entry strategy is based on:

### BUY

A BUY signal requires:

```text
SMA 20 bullish crossover above SMA 50
AND
MACD bullish
AND
RSI between 50 and 70
