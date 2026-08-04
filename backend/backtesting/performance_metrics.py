class PerformanceMetrics:

    def calculate(self, trades):

        completed_trades = []

        for trade in trades:

            if (
                trade.get("type") == "SELL"
                and "profit_loss" in trade
            ):

                completed_trades.append(
                    trade
                )

        total_trades = len(
            completed_trades
        )

        winning_trades = []

        losing_trades = []

        for trade in completed_trades:

            profit_loss = trade[
                "profit_loss"
            ]

            if profit_loss > 0:

                winning_trades.append(
                    profit_loss
                )

            elif profit_loss < 0:

                losing_trades.append(
                    profit_loss
                )

        winning_count = len(
            winning_trades
        )

        losing_count = len(
            losing_trades
        )

        if total_trades > 0:

            win_rate = (

                winning_count
                / total_trades

            ) * 100

        else:

            win_rate = 0

        if winning_trades:

            average_win = (

                sum(winning_trades)
                / len(winning_trades)

            )

            largest_win = max(
                winning_trades
            )

        else:

            average_win = 0

            largest_win = 0

        if losing_trades:

            average_loss = (

                sum(losing_trades)
                / len(losing_trades)

            )

            largest_loss = min(
                losing_trades
            )

        else:

            average_loss = 0

            largest_loss = 0

        total_profit = sum(
            winning_trades
        )

        total_loss = abs(
            sum(losing_trades)
        )

        if total_loss > 0:

            profit_factor = (

                total_profit
                / total_loss

            )

        else:

            profit_factor = 0

        total_realized_profit_loss = (

            total_profit
            - total_loss

        )

        # =========================
        # EXPECTANCY
        # =========================

        loss_rate = 100 - win_rate

        expectancy = (
            (
                win_rate / 100

            )

            * average_win
        ) - (

            (
                loss_rate / 100

            )

            * abs(average_loss)
        )

        return {

            "total_trades": total_trades,

            "winning_trades": winning_count,

            "losing_trades": losing_count,

            "win_rate": round(
                win_rate,
                2
            ),

            "average_win": round(
                average_win,
                2
            ),

            "average_loss": round(
                average_loss,
                2
            ),

            "largest_win": round(
                largest_win,
                2
            ),

            "largest_loss": round(
                largest_loss,
                2
            ),

            "profit_factor": round(
                profit_factor,
                2
            ),

            "expectancy": round(
                expectancy,
                2
            ),

            "total_realized_profit_loss": round(
                total_realized_profit_loss,
                2
            )

        }