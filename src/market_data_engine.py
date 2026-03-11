import yfinance as yf
import pandas as pd
from datetime import datetime
from config.tickers import ALL_TICKERS


class MarketDataEngine:

    def __init__(self):
        self.tickers = ALL_TICKERS

    def fetch_price(self, ticker):
        """
        Fetch latest price and daily change
        """
        try:
            data = yf.Ticker(ticker)
            hist = data.history(period="2d")

            if len(hist) < 2:
                return None, None

            last_close = hist["Close"].iloc[-1]
            prev_close = hist["Close"].iloc[-2]

            change = ((last_close - prev_close) / prev_close) * 100

            return round(last_close, 2), round(change, 2)

        except Exception:
            return None, None

    def fetch_all_markets(self):
        """
        Fetch all configured assets
        """

        results = []

        for name, ticker in self.tickers.items():

            price, change = self.fetch_price(ticker)

            results.append({
                "asset": name,
                "ticker": ticker,
                "price": price,
                "change": change
            })

        df = pd.DataFrame(results)

        return df

    def snapshot(self):
        """
        Market snapshot with timestamp
        """

        df = self.fetch_all_markets()

        data = {}

        for _, row in df.iterrows():

            data[row["asset"]] = {
                "ticker": row["ticker"],
                "price": row["price"],
                "change": row["change"]
            }

        snapshot = {
            "timestamp": datetime.now(),
            "data": data
        }

        return snapshot
