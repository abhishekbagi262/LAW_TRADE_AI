import yfinance as yf
import ta

from backend.backtesting.performance_metrics import (
    PerformanceMetrics
)


class PortfolioBacktester:

    def __init__(
        self,
        starting_balance=100000,
        stop_loss_percent=5,
        take_profit_percent=10,
        position_size_percent=20
    ):

        self.starting_balance = starting_balance
        self.balance = starting_balance

        self.stop_loss_percent = stop_loss_percent
        self.take_profit_percent = take_profit_percent
        self.position_size_percent = position_size_percent

        self.portfolio = {}
        self.trades = []
        self.equity_curve = []

        self.performance_metrics = (
            PerformanceMetrics()
        )

    # =========================
    # DOWNLOAD DATA
    # =========================

    def get_data(
        self,
        symbol,
        period="1y"
    ):

        stock = yf.Ticker(symbol)

        data = stock.history(
            period=period
        )

        if data.empty:

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

        return data

    # =========================
    # BUY
    # =========================

    def buy(
        self,
        symbol,
        price,
        date
    ):

        if symbol in self.portfolio:

            return

        investment_amount = (

            self.balance
            * self.position_size_percent
            / 100

        )

        quantity = int(

            investment_amount
            / price

        )

        if quantity <= 0:

            return

        total_cost = (

            quantity
            * price

        )

        if total_cost > self.balance:

            return

        self.balance -= total_cost

        self.portfolio[symbol] = {

            "quantity": quantity,

            "buy_price": price,

            "buy_date": date

        }

        self.trades.append({

            "type": "BUY",

            "symbol": symbol,

            "date": date,

            "price": round(
                price,
                2
            ),

            "quantity": quantity

        })

    # =========================
    # SELL
    # =========================

    def sell(
        self,
        symbol,
        price,
        date,
        reason
    ):

        if symbol not in self.portfolio:

            return

        position = (

            self.portfolio[symbol]

        )

        quantity = (

            position["quantity"]

        )

        buy_price = (

            position["buy_price"]

        )

        total_value = (

            quantity
            * price

        )

        profit_loss = (

            price
            - buy_price

        ) * quantity

        self.balance += total_value

        self.trades.append({

            "type": "SELL",

            "symbol": symbol,

            "date": date,

            "price": round(
                price,
                2
            ),

            "quantity": quantity,

            "profit_loss": round(
                profit_loss,
                2
            ),

            "reason": reason

        })

        del self.portfolio[symbol]

    # =========================
    # RUN BACKTEST
    # =========================

    def run(
        self,
        symbols,
        period="1y"
    ):

        print(
            "\nDownloading portfolio data..."
        )

        all_data = {}

        for symbol in symbols:

            print(
                f"Downloading data for {symbol}..."
            )

            data = self.get_data(

                symbol,
                period

            )

            if data is not None:

                all_data[symbol] = data

        if not all_data:

            print(
                "No data available."
            )

            return None

        # =========================
        # ALL DATES
        # =========================

        all_dates = set()

        for data in all_data.values():

            all_dates.update(

                data.index

            )

        all_dates = sorted(

            all_dates

        )

        # =========================
        # DAILY SIMULATION
        # =========================

        for current_date in all_dates:

            for symbol, data in (
                all_data.items()
            ):

                if current_date not in data.index:

                    continue

                index = data.index.get_loc(

                    current_date

                )

                if index == 0:

                    continue

                row = data.loc[
                    current_date
                ]

                previous_row = data.iloc[
                    index - 1
                ]

                price = float(

                    row["Close"]

                )

                sma_20 = float(

                    row["SMA_20"]

                )

                sma_50 = float(

                    row["SMA_50"]

                )

                previous_sma_20 = float(

                    previous_row[
                        "SMA_20"
                    ]

                )

                previous_sma_50 = float(

                    previous_row[
                        "SMA_50"
                    ]

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

                date = str(

                    current_date.date()

                )

                # =========================
                # CROSSOVER
                # =========================

                bullish_crossover = (

                    previous_sma_20
                    <= previous_sma_50

                    and sma_20
                    > sma_50

                )

                bearish_crossover = (

                    previous_sma_20
                    >= previous_sma_50

                    and sma_20
                    < sma_50

                )

                # =========================
                # BUY SIGNAL
                # =========================

                buy_signal = (

                    bullish_crossover

                    and macd_value
                    > macd_signal

                    and rsi
                    < 70

                )

                # =========================
                # SELL SIGNAL
                # =========================

                sell_signal = (

                    bearish_crossover

                    or macd_value
                    < macd_signal

                    or rsi
                    > 70

                )

                # =========================
                # EXISTING POSITION
                # =========================

                if symbol in self.portfolio:

                    position = (

                        self.portfolio[
                            symbol
                        ]

                    )

                    buy_price = (

                        position[
                            "buy_price"
                        ]

                    )

                    stop_loss_price = (

                        buy_price

                        * (

                            1

                            - self.stop_loss_percent
                            / 100

                        )

                    )

                    take_profit_price = (

                        buy_price

                        * (

                            1

                            + self.take_profit_percent
                            / 100

                        )

                    )

                    stop_loss_hit = (

                        price
                        <= stop_loss_price

                    )

                    take_profit_hit = (

                        price
                        >= take_profit_price

                    )

                    if stop_loss_hit:

                        self.sell(

                            symbol,

                            price,

                            date,

                            "STOP LOSS"

                        )

                    elif take_profit_hit:

                        self.sell(

                            symbol,

                            price,

                            date,

                            "TAKE PROFIT"

                        )

                    elif sell_signal:

                        self.sell(

                            symbol,

                            price,

                            date,

                            "SIGNAL"

                        )

                # =========================
                # NEW BUY
                # =========================

                elif buy_signal:

                    self.buy(

                        symbol,

                        price,

                        date

                    )

            # =========================
            # PORTFOLIO VALUE
            # =========================

            portfolio_value = 0

            for symbol, position in (

                self.portfolio.items()

            ):

                if symbol not in all_data:

                    continue

                data = all_data[symbol]

                available_data = data[

                    data.index
                    <= current_date

                ]

                if available_data.empty:

                    continue

                current_price = float(

                    available_data.iloc[
                        -1
                    ]["Close"]

                )

                portfolio_value += (

                    current_price

                    * position[
                        "quantity"
                    ]

                )

            total_equity = (

                self.balance
                + portfolio_value

            )

            self.equity_curve.append({

                "date": str(

                    current_date.date()

                ),

                "equity": round(

                    total_equity,

                    2

                )

            })

        # =========================
        # CLOSE OPEN POSITIONS
        # =========================

        for symbol in list(

            self.portfolio.keys()

        ):

            data = all_data[symbol]

            final_price = float(

                data.iloc[-1]["Close"]

            )

            final_date = str(

                data.index[-1].date()

            )

            self.sell(

                symbol,

                final_price,

                final_date,

                "END OF BACKTEST"

            )

        # =========================
        # FINAL PERFORMANCE
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

        # =========================
        # MAXIMUM DRAWDOWN
        # =========================

        peak = (

            self.starting_balance

        )

        maximum_drawdown = 0

        for point in (

            self.equity_curve

        ):

            equity = (

                point["equity"]

            )

            if equity > peak:

                peak = equity

            drawdown = (

                peak
                - equity

            )

            if drawdown > maximum_drawdown:

                maximum_drawdown = (

                    drawdown

                )

        maximum_drawdown_percent = (

            maximum_drawdown

            / self.starting_balance

        ) * 100

        # =========================
        # PERFORMANCE METRICS
        # =========================

        performance = (

            self.performance_metrics.calculate(

                self.trades

            )

        )

        # =========================
        # FINAL RESULT
        # =========================

        return {

            "starting_balance": round(

                self.starting_balance,

                2

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

            "maximum_drawdown": round(

                maximum_drawdown,

                2

            ),

            "maximum_drawdown_percent": round(

                maximum_drawdown_percent,

                2

            ),

            "total_trades": len(

                self.trades

            ),

            "winning_trades": (

                performance[
                    "winning_trades"
                ]

            ),

            "losing_trades": (

                performance[
                    "losing_trades"
                ]

            ),

            "performance": performance,

            "trades": self.trades,

            "equity_curve": (

                self.equity_curve

            )

        }