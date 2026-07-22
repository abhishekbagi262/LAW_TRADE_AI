import json
import os


class PaperTrading:

    def __init__(
        self,
        starting_balance=100000,
        file_name="paper_trading_data.json"
    ):

        self.starting_balance = starting_balance
        self.file_name = file_name

        self.balance = starting_balance
        self.portfolio = {}
        self.trade_history = []

        self.load_data()


    def load_data(self):

        if os.path.exists(self.file_name):

            try:

                with open(
                    self.file_name,
                    "r"
                ) as file:

                    data = json.load(file)


                self.balance = data.get(
                    "balance",
                    self.starting_balance
                )


                self.portfolio = data.get(
                    "portfolio",
                    {}
                )


                self.trade_history = data.get(
                    "trade_history",
                    []
                )


            except:

                print(
                    "Could not load paper trading data."
                )


    def save_data(self):

        data = {

            "balance": self.balance,

            "portfolio": self.portfolio,

            "trade_history": self.trade_history

        }


        with open(
            self.file_name,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )


    def buy(
        self,
        symbol,
        price,
        quantity
    ):

        total_cost = (
            price * quantity
        )


        if total_cost > self.balance:

            return (
                "Insufficient virtual balance."
            )


        self.balance -= total_cost


        if symbol in self.portfolio:

            old_quantity = (
                self.portfolio[symbol]
                ["quantity"]
            )


            old_average_price = (
                self.portfolio[symbol]
                ["average_price"]
            )


            new_quantity = (
                old_quantity + quantity
            )


            new_average_price = (

                (

                    old_average_price
                    * old_quantity

                )

                +

                (

                    price
                    * quantity

                )

            ) / new_quantity


            self.portfolio[symbol] = {

                "quantity": new_quantity,

                "average_price": round(
                    new_average_price,
                    2
                )

            }


        else:

            self.portfolio[symbol] = {

                "quantity": quantity,

                "average_price": price

            }


        self.trade_history.append({

            "type": "BUY",

            "symbol": symbol,

            "price": price,

            "quantity": quantity

        })


        self.save_data()


        return (

            f"Bought {quantity} shares "
            f"of {symbol}"

        )


    def sell(
        self,
        symbol,
        price,
        quantity
    ):

        if symbol not in self.portfolio:

            return (
                "You do not own this stock."
            )


        owned_quantity = (

            self.portfolio[symbol]
            ["quantity"]

        )


        if owned_quantity < quantity:

            return (
                "Not enough shares to sell."
            )


        average_price = (

            self.portfolio[symbol]
            ["average_price"]

        )


        profit_loss = (

            price - average_price

        ) * quantity


        self.balance += (

            price * quantity

        )


        remaining_quantity = (

            owned_quantity - quantity

        )


        if remaining_quantity == 0:

            del self.portfolio[symbol]

        else:

            self.portfolio[symbol][
                "quantity"
            ] = remaining_quantity


        self.trade_history.append({

            "type": "SELL",

            "symbol": symbol,

            "price": price,

            "quantity": quantity,

            "profit_loss": round(
                profit_loss,
                2
            )

        })


        self.save_data()


        return (

            f"Sold {quantity} shares "
            f"of {symbol}. "

            f"P/L: ₹{profit_loss:.2f}"

        )


    def get_portfolio(self):

        return self.portfolio


    def get_balance(self):

        return self.balance


    def get_trade_history(self):

        return self.trade_history