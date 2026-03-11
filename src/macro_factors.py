# src/macro_factors.py

class MacroFactorModel:

    def __init__(self, market_df):
        """
        market_df: dataframe produced by MarketDataEngine
        """
        self.df = market_df.set_index("asset")

    def get_value(self, asset):
        """
        Safely extract price and change
        """
        try:
            price = self.df.loc[asset]["price"]
            change = self.df.loc[asset]["change"]
            return price, change
        except Exception:
            return None, None


    def detect_energy_shock(self):
        """
        Oil shock detection
        """
        price, change = self.get_value("OIL")

        if change is None:
            return False

        if abs(change) > 5:
            return True

        return False


    def detect_safe_haven(self):
        """
        Gold rally + Nasdaq weakness
        """
        gold_price, gold_change = self.get_value("GOLD")
        nasdaq_price, nasdaq_change = self.get_value("NASDAQ")

        if gold_change is None or nasdaq_change is None:
            return False

        if gold_change > 1.5 and nasdaq_change < 0:
            return True

        return False


    def detect_volatility_stress(self):
        """
        VIX spike detection
        """
        price, change = self.get_value("VIX")

        if price is None:
            return False

        if price > 25:
            return True

        return False


    def detect_risk_on(self):
        """
        Risk-on environment
        """
        nasdaq_price, nasdaq_change = self.get_value("NASDAQ")
        vix_price, vix_change = self.get_value("VIX")

        if nasdaq_change is None or vix_price is None:
            return False

        if nasdaq_change > 1 and vix_price < 18:
            return True

        return False


    def market_regime(self):
        """
        Determine overall market regime
        """

        if self.detect_energy_shock():
            return "ENERGY SHOCK"

        if self.detect_volatility_stress():
            return "VOLATILITY STRESS"

        if self.detect_safe_haven():
            return "SAFE HAVEN FLOW"

        if self.detect_risk_on():
            return "RISK ON"

        return "NEUTRAL"
