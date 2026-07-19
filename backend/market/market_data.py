import yfinance as yf


class MarketData:
    def get_stock_data(self, symbol, period="1mo"):
        stock = yf.Ticker(symbol)
        return stock.history(period=period)

    def get_current_price(self, symbol):
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")

        if data.empty:
            return None

        return round(data["Close"].iloc[-1], 2)