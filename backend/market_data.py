import yfinance as yf


class MarketData:

    def get_stock_data(self, symbol, period="1mo"):
        stock = yf.Ticker(symbol)
        data = stock.history(period=period)
        return data


if __name__ == "__main__":

    market = MarketData()

    symbol = input("Enter NSE Stock Symbol (Example: RELIANCE.NS): ").strip().upper()

    data = market.get_stock_data(symbol)

    if data.empty:
        print("\nNo data found. Check the stock symbol.")
    else:
        print("\nLatest Market Data:\n")
        print(data.tail())