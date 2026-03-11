# src/database_storage.py

import sqlite3
import pandas as pd
from datetime import datetime


class DatabaseStorage:

    def __init__(self, db_path="macro_terminal.db"):
        """
        Initialize database connection
        """
        self.conn = sqlite3.connect(db_path)
        self.create_tables()


    def create_tables(self):
        """
        Create required tables
        """

        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS market_snapshots (
            timestamp TEXT,
            asset TEXT,
            ticker TEXT,
            price REAL,
            change REAL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_rankings (
            timestamp TEXT,
            asset TEXT,
            price REAL,
            change REAL,
            ai_score REAL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS macro_regime (
            timestamp TEXT,
            regime TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS energy_projection (
            timestamp TEXT,
            company TEXT,
            current_price REAL,
            oil_change REAL,
            projected_price REAL
        )
        """)

        self.conn.commit()


    def store_market_snapshot(self, market_df):
        """
        Store market snapshot
        """

        timestamp = str(datetime.now())

        df = market_df.copy()
        df["timestamp"] = timestamp

        df = df[["timestamp", "asset", "ticker", "price", "change"]]

        df.to_sql(
            "market_snapshots",
            self.conn,
            if_exists="append",
            index=False
        )


    def store_ai_ranking(self, ranking_df):

        timestamp = str(datetime.now())

        df = ranking_df.copy()
        df["timestamp"] = timestamp

        df = df[["timestamp", "asset", "price", "change", "ai_score"]]

        df.to_sql(
            "ai_rankings",
            self.conn,
            if_exists="append",
            index=False
        )


    def store_macro_regime(self, regime):

        cursor = self.conn.cursor()

        cursor.execute("""
        INSERT INTO macro_regime
        VALUES (?, ?)
        """, (str(datetime.now()), regime))

        self.conn.commit()


    def store_energy_projection(self, projections):

        timestamp = str(datetime.now())

        df = pd.DataFrame(projections)

        df["timestamp"] = timestamp

        df = df[[
            "timestamp",
            "company",
            "current_price",
            "oil_change",
            "projected_price"
        ]]

        df.to_sql(
            "energy_projection",
            self.conn,
            if_exists="append",
            index=False
        )


    def close(self):
        self.conn.close()
