import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path="macro_terminal.db"):
        self.db_path = os.path.join(os.getcwd(), db_path)
        self.initialize_db()

    def initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS macro_signals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    regime TEXT,
                    energy_signal TEXT
                )
            """)
            conn.commit()

    def save_snapshot(self, regime, energy_signal):
        try:
            # We open and close the connection for every save to force a disk write
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO macro_signals (regime, energy_signal) VALUES (?, ?)",
                (str(regime), str(energy_signal))
            )
            conn.commit()
            conn.close()
            # This confirmation is vital:
            print(f" -- [DB] Snapshot saved to {self.db_path} at {regime}")
        except Exception as e:
            print(f" -- [DB] Error: {e}")
