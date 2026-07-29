from backend import config


class RiskManager:

    def calculate_stop_loss(self, entry_price):

         stop_loss = entry_price * (1 - config.STOP_LOSS_PERCENTAGE)

         return round(stop_loss, 2)

    def calculate_position_size(self, balance, entry_price, stop_loss):

        risk_amount = balance * config.MAX_RISK_PER_TRADE

        risk_per_share = abs(entry_price - stop_loss)

        if risk_per_share == 0:
            return 0

        quantity = int(risk_amount / risk_per_share)

        return max(quantity, 1)