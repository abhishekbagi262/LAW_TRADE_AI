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

                with open(self.file_name, "r") as file:

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

            except Exception as error:

                print(
                    f"Could not load paper trading data: {error}"
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

        total_cost = price * quantity

        if total_cost > self.balance:

            return "Insufficient virtual balance."


        self.balance -= total_cost


        if symbol in self.portfolio:

            old_quantity = (
                self.portfolio[symbol]["quantity"]
            )

            old_average_price = (
                self.portfolio[symbol]["average_price"]
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

            return "You do not own this stock."


        owned_quantity = (
            self.portfolio[symbol]["quantity"]
        )


        if owned_quantity < quantity:

            return "Not enough shares to sell."


        average_price = (
            self.portfolio[symbol]["average_price"]
        )


        profit_loss = (
            price - average_price
        ) * quantity


        self.balance += price * quantity


        remaining_quantity = (
            owned_quantity - quantity
        )


        if remaining_quantity == 0:

            del self.portfolio[symbol]

        else:

            self.portfolio[symbol]["quantity"] = (
                remaining_quantity
            )


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


    def get_portfolio_value(self, market):

        portfolio_value = 0

        portfolio_details = {}


        for symbol, data in self.portfolio.items():

            current_price = (
                market.get_current_price(symbol)
            )


            if current_price is None:

                continue


            quantity = data["quantity"]

            average_price = data["average_price"]


            current_value = (
                current_price * quantity
            )


            invested_value = (
                average_price * quantity
            )


            profit_loss = (
                current_value - invested_value
            )


            if invested_value != 0:

                return_percent = (

                    profit_loss
                    / invested_value

                ) * 100

            else:

                return_percent = 0


            portfolio_value += current_value


            portfolio_details[symbol] = {

                "quantity": quantity,

                "average_price": average_price,

                "current_price": current_price,

                "current_value": round(
                    current_value,
                    2
                ),

                "profit_loss": round(
                    profit_loss,
                    2
                ),

                "return_percent": round(
                    return_percent,
                    2
                )

            }


        return {

            "total_value": round(
                portfolio_value,
                2
            ),

            "holdings": portfolio_details

        }


    def get_portfolio(self):

        return self.portfolio


    def get_balance(self):

        return self.balance


    def get_trade_history(self):

        return self.trade_history