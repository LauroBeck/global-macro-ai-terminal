# src/energy_shock_model.py

class EnergyShockModel:

    def __init__(self, market_df):
        """
        market_df: dataframe from MarketDataEngine
        """
        self.df = market_df.set_index("asset")


    def get_asset(self, name):
        """
        Safely extract asset data
        """
        try:
            price = self.df.loc[name]["price"]
            change = self.df.loc[name]["change"]
            return price, change
        except Exception:
            return None, None


    def oil_shock_score(self):
        """
        Measure intensity of oil movement
        """
        oil_price, oil_change = self.get_asset("OIL")

        if oil_change is None:
            return 0

        if abs(oil_change) < 2:
            return 1

        if abs(oil_change) < 5:
            return 2

        if abs(oil_change) < 10:
            return 3

        return 4


    def energy_sector_projection(self):
        """
        Estimate energy company upside if oil surges
        """

        oil_price, oil_change = self.get_asset("OIL")

        energy_assets = [
            "CHEVRON",
            "EXXON",
            "BP",
            "SHELL",
            "CONOCOPHILLIPS"
        ]

        projections = []

        for company in energy_assets:

            price, change = self.get_asset(company)

            if price is None:
                continue

            # simple elasticity model
            projected = price * (1 + (oil_change / 100) * 0.6)

            projections.append({
                "company": company,
                "current_price": price,
                "oil_change": oil_change,
                "projected_price": round(projected, 2)
            })

        return projections


    def macro_energy_signal(self):
        """
        Classify oil market regime
        """

        oil_price, oil_change = self.get_asset("OIL")

        if oil_change is None:
            return "UNKNOWN"

        if oil_change > 7:
            return "SUPPLY SHOCK"

        if oil_change > 3:
            return "OIL RALLY"

        if oil_change < -5:
            return "DEMAND COLLAPSE"

        return "NORMAL"
