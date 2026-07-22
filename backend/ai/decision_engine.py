class DecisionEngine:

    def generate_signal(self, fundamental, technical):

        score = 0
        reasons = []

        # =========================
        # FUNDAMENTAL ANALYSIS
        # =========================

        pe = fundamental.get("pe_ratio")

        if pe is not None:

            if pe < 20:
                score += 2
                reasons.append("P/E ratio is relatively attractive")

            elif pe > 40:
                score -= 2
                reasons.append("P/E ratio is relatively high")

        profit_margin = fundamental.get("profit_margin")

        if profit_margin is not None:

            if profit_margin > 0.10:
                score += 2
                reasons.append("Healthy profit margin")

            elif profit_margin < 0:
                score -= 2
                reasons.append("Negative profit margin")

        revenue_growth = fundamental.get("revenue_growth")

        if revenue_growth is not None:

            if revenue_growth > 0.10:
                score += 2
                reasons.append("Strong revenue growth")

            elif revenue_growth < 0:
                score -= 2
                reasons.append("Negative revenue growth")

        earnings_growth = fundamental.get("earnings_growth")

        if earnings_growth is not None:

            if earnings_growth > 0.10:
                score += 2
                reasons.append("Strong earnings growth")

            elif earnings_growth < 0:
                score -= 2
                reasons.append("Negative earnings growth")

        # =========================
        # TECHNICAL ANALYSIS
        # =========================

        trend = technical.get("trend")

        if trend == "UPTREND":
            score += 2
            reasons.append("Technical trend is bullish")

        elif trend == "DOWNTREND":
            score -= 2
            reasons.append("Technical trend is bearish")

        rsi_signal = technical.get("rsi_signal")

        if rsi_signal == "OVERSOLD":
            score += 1
            reasons.append("Stock may be technically oversold")

        elif rsi_signal == "OVERBOUGHT":
            score -= 1
            reasons.append("Stock may be technically overbought")

        macd_trend = technical.get("macd_trend")

        if macd_trend == "BULLISH":
            score += 2
            reasons.append("MACD indicates bullish momentum")

        elif macd_trend == "BEARISH":
            score -= 2
            reasons.append("MACD indicates bearish momentum")

        # =========================
        # FINAL DECISION
        # =========================

        if score >= 5:
            signal = "BUY"

        elif score <= -3:
            signal = "AVOID"

        else:
            signal = "HOLD"

        return {
            "score": score,
            "signal": signal,
            "reasons": reasons
        }