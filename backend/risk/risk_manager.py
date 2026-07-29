from backend import config


class RiskManager:

    def calculate_stop_loss(self, entry_price, atr):

        stop_loss = entry_price - (2 * atr)

        return round(stop_loss, 2)

    def calculate_position_size(self, balance, entry_price, stop_loss):

        risk_amount = balance * config.MAX_RISK_PER_TRADE

        risk_per_share = abs(entry_price - stop_loss)

        if risk_per_share == 0:
            return 0

        quantity = int(risk_amount / risk_per_share)

        return max(quantity, 1)

    def calculate_targets(self, entry_price, stop_loss):
        risk = entry_price - stop_loss

        target1 = entry_price + (2 * risk)

        target2 = entry_price + (4 * risk)

        reward1 = target1 - entry_price
        reward2 = target2 - entry_price

        rr1 = round(reward1 / risk, 2) if risk != 0 else 0
        rr2 = round(reward2 / risk, 2) if risk != 0 else 0

        return {
            "target1": round(target1, 2),
            "target2": round(target2, 2),
            "risk": round(risk, 2),
            "rr1": rr1,
            "rr2": rr2
        }