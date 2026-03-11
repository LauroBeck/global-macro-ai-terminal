# src/charts_engine.py

import matplotlib.pyplot as plt
import pandas as pd


class ChartsEngine:

    def __init__(self):
        pass


    def plot_ai_ranking(self, ranking_df):
        """
        Plot AI ranking bar chart
        """

        assets = ranking_df["asset"]
        scores = ranking_df["ai_score"]

        plt.figure(figsize=(10,6))
        plt.bar(assets, scores)

        plt.title("AI Stock Ranking")
        plt.xlabel("Asset")
        plt.ylabel("AI Score")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.show()


    def plot_market_changes(self, market_df):
        """
        Plot market daily change
        """

        df = market_df.copy()

        df = df.sort_values("change")

        plt.figure(figsize=(10,6))

        plt.barh(df["asset"], df["change"])

        plt.title("Global Market Daily Change %")

        plt.xlabel("Change %")

        plt.tight_layout()

        plt.show()


    def plot_energy_projection(self, projections):
        """
        Plot oil impact on energy companies
        """

        df = pd.DataFrame(projections)

        companies = df["company"]
        current = df["current_price"]
        projected = df["projected_price"]

        x = range(len(companies))

        plt.figure(figsize=(10,6))

        plt.bar(x, current, label="Current")
        plt.bar(x, projected, label="Projected", alpha=0.6)

        plt.xticks(x, companies, rotation=45)

        plt.title("Energy Sector Projection (Oil Impact)")
        plt.ylabel("Price")

        plt.legend()

        plt.tight_layout()

        plt.show()


    def plot_nasdaq_trend(self, market_df):
        """
        Simple Nasdaq visualization
        """

        try:
            nasdaq = market_df[market_df["asset"] == "NASDAQ"]

            price = nasdaq["price"].values[0]
            change = nasdaq["change"].values[0]

            plt.figure(figsize=(6,4))

            plt.bar(["NASDAQ"], [change])

            plt.title(f"Nasdaq Change {change:.2f}% | Price {price}")

            plt.ylabel("Daily Change %")

            plt.tight_layout()

            plt.show()

        except:
            pass
