import yfinance as yf
import ta


class Backtester:

    def __init__(
        self,
        starting_balance=100000,
        stop_loss_percent=7,
        take_profit_percent=10,
        position_size_percent=25,
        transaction_cost_percent=0.1,
        slippage_percent=0.05,
        trailing_stop_percent=7
    ):

        self.starting_balance = starting_balance
        self.stop_loss_percent = stop_loss_percent
        self.take_profit_percent = take_profit_percent
        self.position_size_percent = position_size_percent
        self.transaction_cost_percent = transaction_cost_percent
        self.slippage_percent = slippage_percent
        self.trailing_stop_percent = trailing_stop_percent

        self.balance = starting_balance
        self.shares = 0
        self.buy_price = 0
        self.highest_price = 0

        self.trades = []
        self.equity_curve = []


    # =====================================================
    # PUBLIC BACKTEST METHOD
    # =====================================================

    def run(
        self,
        symbol,
        period="1y"
    ):

        print(
            f"\nDownloading data for {symbol}..."
        )

        stock = yf.Ticker(symbol)

        data = stock.history(
            period=period
        )

        if data.empty:

            print(
                "No historical data found."
            )

            return None

        return self._run_on_data(
            symbol,
            data
        )


    # =====================================================
    # INTERNAL BACKTEST ENGINE
    # =====================================================

    def _run_on_data(
        self,
        symbol,
        data
    ):

        # -------------------------------------------------
        # RESET STATE
        # -------------------------------------------------

        self.balance = self.starting_balance
        self.shares = 0
        self.buy_price = 0
        self.highest_price = 0

        self.trades = []
        self.equity_curve = []


        # -------------------------------------------------
        # COPY DATA
        # -------------------------------------------------

        data = data.copy()


        # -------------------------------------------------
        # TECHNICAL INDICATORS
        # -------------------------------------------------

        data["SMA_20"] = (
            data["Close"]
            .rolling(
                window=20
            )
            .mean()
        )

        data["SMA_50"] = (
            data["Close"]
            .rolling(
                window=50
            )
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

        data["ATR"] = (
            ta.volatility
            .AverageTrueRange(
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                window=14
            )
            .average_true_range()
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

        data["PREVIOUS_SMA_20"] = (
            data["SMA_20"]
            .shift(1)
        )

        data["PREVIOUS_SMA_50"] = (
            data["SMA_50"]
            .shift(1)
        )

        data["PREVIOUS_MACD"] = (
            data["MACD"]
            .shift(1)
        )

        data["PREVIOUS_MACD_SIGNAL"] = (
            data["MACD_SIGNAL"]
            .shift(1)
        )

        data = data.dropna()


        if data.empty:

            print(
                "Not enough data for indicators."
            )

            return None


        # -------------------------------------------------
        # BUY & HOLD BENCHMARK
        # -------------------------------------------------

        buy_and_hold_start_price = float(
            data.iloc[0]["Close"]
        )

        buy_and_hold_end_price = float(
            data.iloc[-1]["Close"]
        )

        buy_and_hold_return_percent = (

            (

                buy_and_hold_end_price
                -
                buy_and_hold_start_price

            )

            /

            buy_and_hold_start_price

        ) * 100


        # -------------------------------------------------
        # HISTORICAL SIMULATION
        # -------------------------------------------------

        for index, row in data.iterrows():

            price = float(
                row["Close"]
            )

            day_high = float(
                row["High"]
            )

            day_low = float(
                row["Low"]
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
            atr = float(
                row["ATR"]
            )

            macd_value = float(
                row["MACD"]
            )

            macd_signal = float(
                row["MACD_SIGNAL"]
            )

            previous_sma_20 = float(
                row["PREVIOUS_SMA_20"]
            )

            previous_sma_50 = float(
                row["PREVIOUS_SMA_50"]
            )

            previous_macd = float(
                row["PREVIOUS_MACD"]
            )

            previous_macd_signal = float(
                row["PREVIOUS_MACD_SIGNAL"]
            )


            # ---------------------------------------------
            # BUY SIGNAL
            # ---------------------------------------------

            bullish_crossover = (

                previous_sma_20
                <=
                previous_sma_50

                and

                sma_20
                >
                sma_50

            )


            trend_is_bullish = (

                sma_20
                >
                sma_50

            )


            macd_bullish = (

                macd_value
                >
                macd_signal

            )


            rsi_is_healthy = (

                rsi >= 50

                and

                rsi <= 70

            )


            buy_signal = (

                bullish_crossover

                and

                macd_bullish

                and

                rsi_is_healthy

            )

            # ---------------------------------------------
            # SELL SIGNAL
            # ---------------------------------------------

            bearish_crossover = (

                previous_sma_20
                >=
                previous_sma_50

                and

                sma_20
                <
                sma_50

            )


            macd_bearish = (

                previous_macd
                >=
                previous_macd_signal

                and

                macd_value
                <
                macd_signal

                and

                rsi
                <
                50

            )


            # =================================================
            # EXISTING POSITION MANAGEMENT
            # =================================================

            if self.shares > 0:


                # ---------------------------------------------
                # UPDATE HIGHEST PRICE
                # ---------------------------------------------

                if day_high > self.highest_price:

                    self.highest_price = day_high


                fixed_stop_loss_price = (
                      self.buy_price
                      *
                      (
                            1
                            -
                            self.stop_loss_percent
                            /
                            100
                      )
                )


                atr_stop_loss_price = (
                      self.buy_price
                      -
                      (
                            atr
                            *
                            2
                      )
                )

                stop_loss_price = min(
                    fixed_stop_loss_price,
                    atr_stop_loss_price
                )
                

                take_profit_price = (

                    self.buy_price

                    *

                    (

                        1
                        +
                        self.take_profit_percent
                        /
                        100

                    )

                )


                trailing_stop_price = (

                    self.highest_price

                    *

                    (

                        1
                        -
                        self.trailing_stop_percent
                        /
                        100

                    )

                )


                # ---------------------------------------------
                # STOP LOSS
                # ---------------------------------------------

                if day_low <= stop_loss_price:

                    actual_sell_price = (

                        stop_loss_price

                        *

                        (

                            1
                            -
                            self.slippage_percent
                            /
                            100

                        )

                    )


                    self._execute_sell(

                        symbol=symbol,

                        index=index,

                        sell_price=actual_sell_price,

                        reason="STOP LOSS"

                    )


                # ---------------------------------------------
                # TAKE PROFIT
                # ---------------------------------------------

                elif day_high >= take_profit_price:

                    actual_sell_price = (

                        take_profit_price

                        *

                        (

                            1
                            -
                            self.slippage_percent
                            /
                            100

                        )

                    )


                    self._execute_sell(

                        symbol=symbol,

                        index=index,

                        sell_price=actual_sell_price,

                        reason="TAKE PROFIT"

                    )


                # ---------------------------------------------
                # TRAILING STOP
                # ---------------------------------------------

                elif (

                    self.highest_price
                    >
                    self.buy_price

                    and

                    day_low
                    <=
                    trailing_stop_price

                ):

                    actual_sell_price = (

                        trailing_stop_price

                        *

                        (

                            1
                            -
                            self.slippage_percent
                            /
                            100

                        )

                    )


                    self._execute_sell(

                        symbol=symbol,

                        index=index,

                        sell_price=actual_sell_price,

                        reason="TRAILING STOP"

                    )


                # ---------------------------------------------
                # SIGNAL EXIT
                # ---------------------------------------------

                elif bearish_crossover:

                    actual_sell_price = (

                        price

                        *

                        (

                            1
                            -
                            self.slippage_percent
                            /
                            100

                        )

                    )


                    self._execute_sell(

                        symbol=symbol,

                        index=index,

                        sell_price=actual_sell_price,

                        reason="SMA BEARISH CROSSOVER"

                    )


            # =================================================
            # NEW POSITION ENTRY
            # =================================================

            if (

                self.shares == 0

                and

                buy_signal

            ):

                investment_amount = (

                    self.balance

                    *

                    (

                        self.position_size_percent
                        /
                        100

                    )

                )


                actual_buy_price = (

                    price

                    *

                    (

                        1
                        +
                        self.slippage_percent
                        /
                        100

                    )

                )


                quantity = int(

                    investment_amount
                    /
                    actual_buy_price

                )


                if quantity > 0:

                    gross_cost = (

                        quantity
                        *
                        actual_buy_price

                    )


                    transaction_cost = (

                        gross_cost

                        *

                        (

                            self.transaction_cost_percent
                            /
                            100

                        )

                    )


                    total_cost = (

                        gross_cost
                        +
                        transaction_cost

                    )


                    if total_cost <= self.balance:

                        self.balance -= total_cost

                        self.shares = quantity

                        self.buy_price = (

                            actual_buy_price

                        )

                        self.highest_price = (

                            day_high

                        )


                        self.trades.append({

                            "type": "BUY",

                            "date": str(

                                index.date()

                            ),

                            "price": round(

                                actual_buy_price,

                                2

                            ),

                            "quantity": quantity,

                            "transaction_cost": round(

                                transaction_cost,

                                2

                            ),

                            "symbol": symbol

                        })


            # ---------------------------------------------
            # EQUITY CURVE
            # ---------------------------------------------

            current_equity = (

                self.balance

                +

                (

                    self.shares
                    *
                    price

                )

            )


            self.equity_curve.append(

                current_equity

            )


        # =================================================
        # CLOSE OPEN POSITION
        # =================================================

        if self.shares > 0:

            final_price = float(

                data.iloc[-1]["Close"]

            )


            actual_sell_price = (

                final_price

                *

                (

                    1
                    -
                    self.slippage_percent
                    /
                    100

                )

            )


            self._execute_sell(

                symbol=symbol,

                index=data.index[-1],

                sell_price=actual_sell_price,

                reason="END OF BACKTEST"

            )


        # =================================================
        # PERFORMANCE
        # =================================================

        final_balance = self.balance

        total_return = (

            final_balance
            -
            self.starting_balance

        )


        return_percent = (

            total_return
            /
            self.starting_balance

        ) * 100


        # =================================================
        # MAXIMUM DRAWDOWN
        # =================================================

        peak = self.starting_balance

        maximum_drawdown = 0


        for equity in self.equity_curve:

            if equity > peak:

                peak = equity


            drawdown = peak - equity


            if drawdown > maximum_drawdown:

                maximum_drawdown = drawdown


        maximum_drawdown_percent = (

            maximum_drawdown
            /
            self.starting_balance

        ) * 100


        # =================================================
        # TRADE STATISTICS
        # =================================================

        winning_trades = 0

        losing_trades = 0

        total_transaction_costs = 0


        for trade in self.trades:

            total_transaction_costs += (

                trade.get(

                    "transaction_cost",

                    0

                )

            )


            if "profit_loss" in trade:

                if trade["profit_loss"] > 0:

                    winning_trades += 1

                elif trade["profit_loss"] < 0:

                    losing_trades += 1
        total_completed_trades = (
            winning_trades
            +
            losing_trades
        )

        if total_completed_trades > 0:
            win_rate = round(
                (
                    winning_trades
                    /
                    total_completed_trades
                ) * 100,
                2
            )

        else:
            win_rate = 0


        return {

            "symbol": symbol,

            "starting_balance":

                self.starting_balance,

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

            "winning_trades":

                winning_trades,

            "losing_trades":

                losing_trades,

            "win_rate": win_rate,

            "total_transaction_costs": round(

                total_transaction_costs,

                2

            ),

            "trades": self.trades,

            "equity_curve":

                self.equity_curve,

            "buy_and_hold_start_price": round(

                buy_and_hold_start_price,

                2

            ),

            "buy_and_hold_end_price": round(

                buy_and_hold_end_price,

                2

            ),

            "buy_and_hold_return_percent": round(

                buy_and_hold_return_percent,

                2

            )

        }


    # =====================================================
    # SELL EXECUTION HELPER
    # =====================================================

    def _execute_sell(

        self,

        symbol,

        index,

        sell_price,

        reason

    ):

        gross_value = (

            self.shares
            *
            sell_price

        )


        transaction_cost = (

            gross_value

            *

            (

                self.transaction_cost_percent
                /
                100

            )

        )


        net_value = (

            gross_value
            -
            transaction_cost

        )


        profit_loss = (

            net_value

            -

            (

                self.buy_price
                *
                self.shares

            )

        )


        self.balance += net_value


        self.trades.append({

            "type": "SELL",

            "date": str(

                index.date()

            ),

            "price": round(

                sell_price,

                2

            ),

            "quantity": self.shares,

            "profit_loss": round(

                profit_loss,

                2

            ),

            "transaction_cost": round(

                transaction_cost,

                2

            ),

            "reason": reason,

            "symbol": symbol

        })


        self.shares = 0

        self.buy_price = 0

        self.highest_price = 0


    # =====================================================
    # WALK-FORWARD TESTING
    # =====================================================

    def run_walk_forward(

        self,

        symbol,

        period="5y",

        train_ratio=0.60

    ):

        print(

            f"\nDownloading data for {symbol}..."

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


        if (

            train_ratio <= 0

            or

            train_ratio >= 1

        ):

            print(

                "train_ratio must be between 0 and 1."

            )

            return None


        split_index = int(

            len(data)
            *
            train_ratio

        )


        training_data = data.iloc[

            :split_index

        ]


        testing_data = data.iloc[

            split_index:

        ]


        if (

            training_data.empty

            or

            testing_data.empty

        ):

            print(

                "Not enough data."

            )

            return None


        training_start = (

            training_data.index[0]

        )


        training_end = (

            training_data.index[-1]

        )


        testing_start = (

            testing_data.index[0]

        )


        testing_end = (

            testing_data.index[-1]

        )


        training_buy_hold_return = (

            (

                float(

                    training_data.iloc[-1]["Close"]

                )

                -

                float(

                    training_data.iloc[0]["Close"]

                )

            )

            /

            float(

                training_data.iloc[0]["Close"]

            )

        ) * 100


        testing_buy_hold_return = (

            (

                float(

                    testing_data.iloc[-1]["Close"]

                )

                -

                float(

                    testing_data.iloc[0]["Close"]

                )

            )

            /

            float(

                testing_data.iloc[0]["Close"]

            )

        ) * 100


        training_backtester = Backtester(

            starting_balance=self.starting_balance,

            stop_loss_percent=self.stop_loss_percent,

            take_profit_percent=self.take_profit_percent,

            position_size_percent=self.position_size_percent,

            transaction_cost_percent=self.transaction_cost_percent,

            slippage_percent=self.slippage_percent,

            trailing_stop_percent=self.trailing_stop_percent

        )


        training_result = (

            training_backtester._run_on_data(

                symbol,

                training_data

            )

        )


        testing_backtester = Backtester(

            starting_balance=self.starting_balance,

            stop_loss_percent=self.stop_loss_percent,

            take_profit_percent=self.take_profit_percent,

            position_size_percent=self.position_size_percent,

            transaction_cost_percent=self.transaction_cost_percent,

            slippage_percent=self.slippage_percent,

            trailing_stop_percent=self.trailing_stop_percent

        )


        testing_result = (

            testing_backtester._run_on_data(

                symbol,

                testing_data

            )

        )


        if (

            training_result is None

            or

            testing_result is None

        ):

            return None


        training_strategy_return = (

            training_result[

                "return_percent"

            ]

        )


        testing_strategy_return = (

            testing_result[

                "return_percent"

            ]

        )


        print(

            "\n=============================="

        )


        print(

            "WALK-FORWARD TEST"

        )


        print(

            "=============================="

        )


        print(

            "\nTRAINING PERIOD"

        )


        print(

            f"Start: {training_start.date()}"

        )


        print(

            f"End: {training_end.date()}"

        )


        print(

            f"Days: {len(training_data)}"

        )


        print(

            "\nTESTING PERIOD"

        )


        print(

            f"Start: {testing_start.date()}"

        )


        print(

            f"End: {testing_end.date()}"

        )


        print(

            f"Days: {len(testing_data)}"

        )


        print(

            "\n=============================="

        )


        print(

            "TRAINING PERFORMANCE"

        )


        print(

            "=============================="

        )


        print(

            f"Strategy Return: "

            f"{round(training_strategy_return, 2)}%"

        )


        print(

            f"Buy & Hold Return: "

            f"{round(training_buy_hold_return, 2)}%"

        )


        print(

            "\n=============================="

        )


        print(

            "TESTING PERFORMANCE"

        )


        print(

            "=============================="

        )


        print(

            f"Strategy Return: "

            f"{round(testing_strategy_return, 2)}%"

        )


        print(

            f"Buy & Hold Return: "

            f"{round(testing_buy_hold_return, 2)}%"

        )


        return {

            "symbol": symbol,

            "training_start":

                str(

                    training_start.date()

                ),

            "training_end":

                str(

                    training_end.date()

                ),

            "testing_start":

                str(

                    testing_start.date()

                ),

            "testing_end":

                str(

                    testing_end.date()

                ),

            "training_days":

                len(

                    training_data

                ),

            "testing_days":

                len(

                    testing_data

                ),

            "training_strategy_return":

                round(

                    training_strategy_return,

                    2

                ),

            "testing_strategy_return":

                round(

                    testing_strategy_return,

                    2

                ),

            "training_buy_and_hold_return":

                round(

                    training_buy_hold_return,

                    2

                ),

            "testing_buy_and_hold_return":

                round(

                    testing_buy_hold_return,

                    2

                )

        }




