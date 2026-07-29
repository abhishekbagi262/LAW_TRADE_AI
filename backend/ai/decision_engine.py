from backend import config
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
            score += 3
            reasons.append("Technical trend is bullish")

        elif trend == "DOWNTREND":
            score -= 3
            reasons.append("Technical trend is bearish")
        


        
        rsi = technical.get("rsi")

        if rsi is not None:
            if rsi < 25:
                score += 2
                reasons.append(f"RSI ({rsi}) indicates a strong oversold opportunity")

            elif rsi < 35:
                score += 1
                reasons.append(f"RSI ({rsi}) indicates a mild oversold condition")

            elif 35 <= rsi <= 65:
                score += 1
                reasons.append(f"RSI ({rsi}) is in a healthy trading range")

            elif rsi <= 75:
                score -= 1
                reasons.append(f"RSI ({rsi}) suggests the stock is becoming overbought")

            else:

                score -= 2
                reasons.append(f"RSI ({rsi}) indicates a strongly overbought condition")
        macd_trend = technical.get("macd_trend")

        if macd_trend == "BULLISH":
            score += 2
            reasons.append("MACD indicates bullish momentum")

        elif macd_trend == "BEARISH":
            score -= 2
            reasons.append("MACD indicates bearish momentum")

        # =========================
        # VOLUME ANALYSIS
        # =========================

        current_volume = technical.get("current_volume")
        average_volume = technical.get("average_volume")

        if current_volume is not None and average_volume is not None:

            if current_volume > average_volume * 1.2:
                score += 1
                reasons.append("Trading volume is above average")

            elif current_volume < average_volume * 0.8:
                score -= 1
                reasons.append("Trading volume is below average")
        

        # =========================
        # FINAL DECISION
        # =========================

        if score >= config.BUY_SCORE:
            signal = "BUY"

        elif score <= config.AVOID_SCORE:
            signal = "AVOID"

        else:
            signal = "HOLD"

                # =========================
        # AI EXPLANATION
        # =========================

        if signal == "BUY":
            explanation = (
                "The stock is showing more positive signals than negative signals. "
                "Fundamental and technical indicators are supporting a bullish outlook."
            )

        elif signal == "AVOID":
            explanation = (
                "The stock is showing more negative signals than positive signals. "
                "Weak fundamentals or bearish technical indicators are creating risk."
            )

        else:
            explanation = (
                "The stock is showing mixed signals. "
                "Positive and negative factors are currently balanced, "
                "so the system recommends HOLD."
            )

        confidence = round((abs(score) / config.MAX_AI_SCORE) * 100, 1)
        if confidence > 100:
            confidence = 100

        return {
    "score": score,
    "confidence": confidence,
    "signal": signal,
    "reasons": reasons,
    "explanation": explanation
}
    def calculate_trade_quality(
            self,
            analysis,
            technical_data,
            targets
        ):
            score = 0

            # Trend
            if technical_data["trend"] == "UPTREND":
                score += 2

            # RSI
            if 35 <= technical_data["rsi"] <= 65:
                score += 1

            # MACD
            if technical_data["macd"] > technical_data["macd_signal"]:
                score += 2

            # Volume
            if technical_data["current_volume"] > technical_data["average_volume"]:
                score += 1
            # Revenue Growth
            if analysis["revenue_growth"] > 10:
                score += 1

            # Earnings Growth
            if analysis["earnings_growth"] > 0:
                score += 1

            # Profit Margin
            if analysis["profit_margin"] > 10:
                score += 1

            # Risk / Reward
            if targets["rr2"] >= 3:
                score += 1

            return score