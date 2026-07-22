import yfinance as yf
import ta


class TechnicalAnalysis:

    def get_technical_analysis(self, symbol, period="1y"):

        stock = yf.Ticker(symbol)
        data = stock.history(period=period)

        if data.empty:
            return None

        data = data.dropna(subset=["Close"])

        # Moving Averages
        data["SMA_20"] = data["Close"].rolling(window=20).mean()
        data["SMA_50"] = data["Close"].rolling(window=50).mean()

        # Remove rows where indicators are not ready
        data = data.dropna(
            subset=["SMA_20", "SMA_50"]
        )

        if data.empty:
            return None

        # RSI
        data["RSI"] = ta.momentum.RSIIndicator(
            close=data["Close"],
            window=14
        ).rsi()

        # MACD
        macd = ta.trend.MACD(data["Close"])

        data["MACD"] = macd.macd()
        data["MACD_Signal"] = macd.macd_signal()

        data = data.dropna(
            subset=["RSI", "MACD", "MACD_Signal"]
        )

        latest = data.iloc[-1]

        current_price = latest["Close"]
        sma_20 = latest["SMA_20"]
        sma_50 = latest["SMA_50"]
        rsi = latest["RSI"]
        macd_value = latest["MACD"]
        macd_signal = latest["MACD_Signal"]

        if current_price > sma_20 and sma_20 > sma_50:
            trend = "UPTREND"

        elif current_price < sma_20 and sma_20 < sma_50:
            trend = "DOWNTREND"

        else:
            trend = "SIDEWAYS"

        if rsi < 30:
            rsi_signal = "OVERSOLD"

        elif rsi > 70:
            rsi_signal = "OVERBOUGHT"

        else:
            rsi_signal = "NEUTRAL"

        if macd_value > macd_signal:
            macd_trend = "BULLISH"

        else:
            macd_trend = "BEARISH"

        return {
            "current_price": round(float(current_price), 2),
            "sma_20": round(float(sma_20), 2),
            "sma_50": round(float(sma_50), 2),
            "rsi": round(float(rsi), 2),
            "rsi_signal": rsi_signal,
            "macd": round(float(macd_value), 2),
            "macd_signal": round(float(macd_signal), 2),
            "macd_trend": macd_trend,
            "trend": trend
        }