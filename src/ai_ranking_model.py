# src/ai_ranking_model.py

import pandas as pd


class AIRankingModel:

    def __init__(self, market_df, macro_regime=None):
        """
        market_df: dataframe from MarketDataEngine
        macro_regime: regime detected by MacroFactorModel
        """
        self.df = market_df.set_index("asset")
        self.regime = macro_regime


    def get_asset(self, name):
        try:
            price = self.df.loc[name]["price"]
            change = self.df.loc[name]["change"]
            return float(price), float(change)
        except Exception:
            return None, None


    def momentum_score(self, change):
        """
        Convert daily change into score
        """
        if change is None:
            return 0

        if change > 3:
            return 25
        if change > 1:
            return 20
        if change > 0:
            return 15
        if change > -1:
            return 10
        if change > -3:
            return 5

        return 0


    def macro_adjustment(self, asset):
        """
        Adjust ranking depending on macro regime
        """

        if self.regime is None:
            return 0

        if self.regime == "RISK ON":

            if asset in ["NVIDIA", "MICROSOFT", "ORACLE"]:
                return 15

        if self.regime == "SAFE HAVEN FLOW":

            if asset == "GOLD":
                return 20

        if self.regime == "ENERGY SHOCK":

            if asset in ["CHEVRON", "EXXON", "BP", "SHELL"]:
                return 20

        if self.regime == "DEMAND COLLAPSE":

            if asset in ["NVIDIA", "MICROSOFT"]:
                return -10

        return 0


    def rank_assets(self):

        assets = [
            "NVIDIA",
            "MICROSOFT",
            "ORACLE",
            "IBM",
            "CHEVRON",
            "EXXON",
            "BP",
            "SHELL",
            "CONOCOPHILLIPS"
        ]

        ranking = []

        for asset in assets:

            price, change = self.get_asset(asset)

            if price is None:
                continue

            score = 50

            score += self.momentum_score(change)

            score += self.macro_adjustment(asset)

            ranking.append({
                "asset": asset,
                "price": round(price, 2),
                "change": round(change, 2),
                "ai_score": score
            })

        df = pd.DataFrame(ranking)

        df = df.sort_values("ai_score", ascending=False)

        return df
