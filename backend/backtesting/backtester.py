import yfinance as yf
import ta


class Backtester:

    def __init__(
        self,
        starting_balance=100000,
        stop_loss_percent=5,
        take_profit_percent=10,
        position_size_percent=25
    ):

        self.starting_balance = (
            starting_balance
        )

        self.stop_loss_percent = (
            stop_loss_percent
        )

        self.take_profit_percent = (
            take_profit_percent
        )

        self.position_size_percent = (
            position_size_percent
        )

        self.balance = (
            starting_balance
        )

        self.shares = 0

        self.buy_price = 0

        self.trades = []


    def run(
        self,
        symbol,
        period="1y"
    ):

        print(
            f"\nDownloading data for "
            f"{symbol}..."
        )


        stock = yf.Ticker(
            symbol
        )


        data = stock.history(
            period=period
        )


        if data.empty:

            print(
                "No historical data found."
            )

            return None


        # =========================
        # TECHNICAL INDICATORS
        # =========================

        data["SMA_20"] = (
            data["Close"]
            .rolling(window=20)
            .mean()
        )


        data["SMA_50"] = (
            data["Close"]
            .rolling(window=50)
            .mean()
        )


        data["RSI"] = (
            ta.momentum
            .RSIIndicator(
                close=data["Close"],
                window=14
            )
            .rsi()
        )


        macd = ta.trend.MACD(
            data["Close"]
        )


        data["MACD"] = (
            macd.macd()
        )


        data["MACD_SIGNAL"] = (
            macd.macd_signal()
        )


        data = data.dropna()


        # =========================
        # HISTORICAL SIMULATION
        # =========================

        for index, row in data.iterrows():

            price = float(
                row["Close"]
            )


            sma_20 = float(
                row["SMA_20"]
            )


            sma_50 = float(
                row["SMA_50"]
            )


            rsi = float(
                row["RSI"]
            )


            macd_value = float(
                row["MACD"]
            )


            macd_signal = float(
                row["MACD_SIGNAL"]
            )


            # =========================
            # BUY CONDITION
            # =========================

            buy_signal = (

                price > sma_20

                and sma_20 > sma_50

                and macd_value > macd_signal

                and rsi < 70

            )


            # =========================
            # SELL CONDITION
            # =========================

            sell_signal = (

                price < sma_20

                or macd_value < macd_signal

                or rsi > 70

            )


            # =========================
            # RISK MANAGEMENT
            # =========================

            stop_loss_price = (

                self.buy_price
                * (
                    1
                    - self.stop_loss_percent
                    / 100
                )

            )


            take_profit_price = (

                self.buy_price
                * (
                    1
                    + self.take_profit_percent
                    / 100
                )

            )


            # =========================
            # BUY
            # =========================

            if buy_signal:

                if self.shares == 0:


                    investment_amount = (

                        self.balance
                        * (
                            self.position_size_percent
                            / 100
                        )

                    )


                    quantity = int(

                        investment_amount
                        / price

                    )


                    if quantity > 0:


                        total_cost = (

                            quantity
                            * price

                        )


                        self.balance -= (

                            total_cost

                        )


                        self.shares = (

                            quantity

                        )


                        self.buy_price = (

                            price

                        )


                        self.trades.append({

                            "type": "BUY",

                            "date": str(

                                index.date()

                            ),

                            "price": round(

                                price,

                                2

                            ),

                            "quantity": (

                                quantity

                            )

                        })


            # =========================
            # SELL
            # =========================

            elif self.shares > 0:


                stop_loss_hit = (

                    price
                    <= stop_loss_price

                )


                take_profit_hit = (

                    price
                    >= take_profit_price

                )


                if (

                    stop_loss_hit

                    or take_profit_hit

                    or sell_signal

                ):


                    total_value = (

                        self.shares
                        * price

                    )


                    profit_loss = (

                        price
                        - self.buy_price

                    ) * self.shares


                    self.balance += (

                        total_value

                    )


                    if stop_loss_hit:

                        exit_reason = (

                            "STOP LOSS"

                        )

                    elif take_profit_hit:

                        exit_reason = (

                            "TAKE PROFIT"

                        )

                    else:

                        exit_reason = (

                            "SIGNAL"

                        )


                    self.trades.append({

                        "type": "SELL",

                        "date": str(

                            index.date()

                        ),

                        "price": round(

                            price,

                            2

                        ),

                        "quantity": (

                            self.shares

                        ),

                        "profit_loss": round(

                            profit_loss,

                            2

                        ),

                        "reason": (

                            exit_reason

                        )

                    })


                    self.shares = 0

                    self.buy_price = 0


        # =========================
        # CLOSE OPEN POSITION
        # =========================

        if self.shares > 0:


            final_price = float(

                data.iloc[-1]["Close"]

            )


            total_value = (

                self.shares
                * final_price

            )


            profit_loss = (

                final_price
                - self.buy_price

            ) * self.shares


            self.balance += (

                total_value

            )


            self.trades.append({

                "type": "FINAL SELL",

                "date": str(

                    data.index[-1].date()

                ),

                "price": round(

                    final_price,

                    2

                ),

                "quantity": (

                    self.shares

                ),

                "profit_loss": round(

                    profit_loss,

                    2

                ),

                "reason": (

                    "END OF BACKTEST"

                )

            })


            self.shares = 0


        # =========================
        # PERFORMANCE
        # =========================

        final_balance = (

            self.balance

        )


        total_return = (

            final_balance

            - self.starting_balance

        )


        return_percent = (

            total_return

            / self.starting_balance

        ) * 100


        winning_trades = 0

        losing_trades = 0


        for trade in self.trades:


            if (

                "profit_loss"

                in trade

            ):


                if (

                    trade[

                        "profit_loss"

                    ]

                    > 0

                ):


                    winning_trades += 1


                elif (

                    trade[

                        "profit_loss"

                    ]

                    < 0

                ):


                    losing_trades += 1


        return {

            "symbol": symbol,

            "starting_balance": (

                self.starting_balance

            ),

            "final_balance": round(

                final_balance,

                2

            ),

            "total_return": round(

                total_return,

                2

            ),

            "return_percent": round(

                return_percent,

                2

            ),

            "total_trades": len(

                self.trades

            ),

            "winning_trades": (

                winning_trades

            ),

            "losing_trades": (

                losing_trades

            ),

            "trades": self.trades

        }