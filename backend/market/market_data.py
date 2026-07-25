import yfinance as yf


class MarketData:

    # =========================
    # GET STOCK DATA
    # =========================

    def get_stock_data(
        self,
        symbol,
        period="1y"
    ):

        try:

            stock = yf.Ticker(
                symbol
            )

            data = stock.history(
                period=period
            )

            return data

        except Exception:

            return None


    # =========================
    # CURRENT PRICE
    # =========================

    def get_current_price(
        self,
        symbol
    ):

        try:

            stock = yf.Ticker(
                symbol
            )

            data = stock.history(
                period="1d"
            )

            if data.empty:

                return None

            price = data["Close"].iloc[-1]

            return round(
                float(price),
                2
            )

        except Exception:

            return None


    # =========================
    # DAY CHANGE
    # =========================

    def get_day_change(
        self,
        symbol
    ):

        try:

            stock = yf.Ticker(
                symbol
            )

            data = stock.history(
                period="2d"
            )

            if len(data) < 2:

                return 0

            previous_close = (

                data["Close"].iloc[-2]

            )


            current_close = (

                data["Close"].iloc[-1]

            )


            change = (

                (

                    current_close

                    - previous_close

                )

                / previous_close

            ) * 100


            return round(

                float(change),

                2

            )

        except Exception:

            return 0


    # =========================
    # COMPANY INFORMATION
    # =========================

    def get_company_info(
        self,
        symbol
    ):

        try:

            stock = yf.Ticker(
                symbol
            )

            info = stock.info

            return info

        except Exception:

            return {}


    # =========================
    # FUNDAMENTAL ANALYSIS DATA
    # =========================

    def get_analysis_data(
        self,
        symbol
    ):

        try:

            stock = yf.Ticker(
                symbol
            )

            info = stock.info


            profit_margin = (

                info.get(
                    "profitMargins"
                )

            )


            revenue_growth = (

                info.get(
                    "revenueGrowth"
                )

            )


            earnings_growth = (

                info.get(
                    "earningsGrowth"
                )

            )


            if profit_margin is not None:

                profit_margin = round(

                    profit_margin * 100,

                    2

                )


            if revenue_growth is not None:

                revenue_growth = round(

                    revenue_growth * 100,

                    2

                )


            if earnings_growth is not None:

                earnings_growth = round(

                    earnings_growth * 100,

                    2

                )


            return {

                "profit_margin": (

                    profit_margin

                ),

                "revenue_growth": (

                    revenue_growth

                ),

                "earnings_growth": (

                    earnings_growth

                )

            }


        except Exception:

            return {

                "profit_margin": None,

                "revenue_growth": None,

                "earnings_growth": None

            }


    # =========================
    # STOCK COMPARISON DATA
    # =========================

    def get_stock_comparison_data(
        self,
        symbol
    ):

        try:

            from backend.backtesting.backtester import Backtester


            backtester = Backtester(

                starting_balance=100000

            )


            result = (

                backtester.run(

                    symbol,

                    period="1y"

                )

            )


            if result is None:

                return None


            return result


        except Exception as error:

            print(

                f"Comparison error for "

                f"{symbol}: "

                f"{error}"

            )

            return None