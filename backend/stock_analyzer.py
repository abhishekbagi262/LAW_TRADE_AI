class StockAnalyzer:

    def __init__(
        self,
        market,
        technical,
        decision_engine,
        risk_manager,
        config
    ):

        self.market = market
        self.technical = technical
        self.decision_engine = decision_engine
        self.risk_manager = risk_manager
        self.config = config

    def analyze_stock(self, symbol):
        price = self.market.get_current_price(symbol)

        if price is None:
            return None

        change = self.market.get_day_change(symbol)

        info = self.market.get_company_info(symbol)

        analysis = self.market.get_analysis_data(symbol)

        technical_data = self.technical.get_technical_analysis(symbol)

        fundamental_data = {
            "pe_ratio": info.get("trailingPE"),

            "profit_margin": analysis.get("profit_margin"),

            "revenue_growth": analysis.get("revenue_growth"),

            "earnings_growth": analysis.get("earnings_growth")
        }

        decision = self.decision_engine.generate_signal(
            fundamental_data,
            technical_data
        )

        entry_price = price
        stop_loss = self.risk_manager.calculate_stop_loss(
            entry_price,
            technical_data["atr"]
        )

        targets = self.risk_manager.calculate_targets(
            entry_price,
            stop_loss
        )

        trade_quality = self.decision_engine.calculate_trade_quality(
            analysis,
            technical_data,
            targets
        )
        

        position_size = self.risk_manager.calculate_position_size(
            self.config.INITIAL_BALANCE,
            entry_price,
            stop_loss

        )

        return {
            "symbol": symbol,

            "price": price,

            "change": change,

            "info": info,

            "analysis": analysis,

            "technical_data": technical_data,

            "decision": decision,

            "entry_price": entry_price,

            "stop_loss": stop_loss,

            "targets": targets,

            "trade_quality": trade_quality,

            "position_size": position_size
        }