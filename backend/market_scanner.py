class MarketScanner:

    def __init__(self, stock_analyzer):

        self.stock_analyzer = stock_analyzer

    def scan_market(self):
        from backend.nifty50 import NIFTY_50
        stocks = NIFTY_50

        results = []

        for stock in stocks:
            stock_data = self.stock_analyzer.analyze_stock(stock)

            if stock_data is None:

                continue
            results.append({
                "Stock": stock,

                "Signal": stock_data["decision"]["signal"],

                "Quality": f'{stock_data["trade_quality"]}/10',

                "Confidence": f'{stock_data["decision"]["confidence"]}%'

            })

        results.sort(
            key=lambda x: (
                float(x["Confidence"].replace("%", "")),
                int(x["Quality"].split("/")[0])
            ),
            reverse=True
        )
        return results
