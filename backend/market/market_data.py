import yfinance as yf


class MarketData:
    def get_stock_data(self, symbol, period="1mo"):
        stock = yf.Ticker(symbol)
        return stock.history(period=period)