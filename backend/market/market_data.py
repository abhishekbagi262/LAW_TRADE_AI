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

    def get_day_change(self, symbol):
        stock = yf.Ticker(symbol)
        data = stock.history(period="5d")

        data = data.dropna(subset=["Close"])

        if len(data) < 2:
            return None

        previous_close = data["Close"].iloc[-2]
        current_close = data["Close"].iloc[-1]

        change_percent = (
            (current_close - previous_close) / previous_close
        ) * 100

        return round(float(change_percent), 2)

    def get_company_info(self, symbol):
        stock = yf.Ticker(symbol)
        return stock.info
    
    def get_financials(self, symbol):
        stock = yf.Ticker(symbol)
        return stock.financials

    def get_balance_sheet(self, symbol):
        stock = yf.Ticker(symbol)
        return stock.balance_sheet

    def get_cashflow(self, symbol):
        stock = yf.Ticker(symbol)
        return stock.cashflow
    def get_pe_ratio(self, symbol):
        stock = yf.Ticker(symbol)
        info = stock.info

        return info.get("trailingPE")    
    def get_eps(self, symbol):
        stock = yf.Ticker(symbol)
        info = stock.info

        return info.get("trailingEps")