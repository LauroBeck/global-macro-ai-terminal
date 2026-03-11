from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from datetime import datetime
import pandas as pd

from src.market_data_engine import MarketDataEngine
from src.macro_factors import MacroFactorModel
from src.energy_shock_model import EnergyShockModel
from src.ai_ranking_model import AIRankingModel

class TerminalDashboard:
    def __init__(self):
        self.console = Console()
        self.engine = MarketDataEngine()

    def safe_float(self, value):
        try:
            return float(value)
        except:
            return 0.0

    def build_market_table(self, data):
        table = Table(title="GLOBAL MARKET SNAPSHOT")
        table.add_column("Asset", style="cyan")
        table.add_column("Ticker")
        table.add_column("Price", justify="right")
        table.add_column("Change %", justify="right")

        for asset, info in data.items():
            if not isinstance(info, dict):
                info = {"price": info, "ticker": asset, "change": 0.0}
            ticker = str(info.get("ticker", asset))
            price = self.safe_float(info.get("price"))
            change = self.safe_float(info.get("change"))
            color = "green" if change >= 0 else "red"
            table.add_row(str(asset), ticker, f"{price:.2f}", f"[{color}]{change:.2f}%[/{color}]")
        return table

    def build_ai_ranking_table(self, rankings):
        table = Table(title="AI MARKET RANKING")
        table.add_column("Rank", justify="center")
        table.add_column("Asset", style="magenta")
        table.add_column("Score", justify="right")

        for i, r in enumerate(rankings):
            if isinstance(r, dict):
                asset_name = r.get("asset", "UNKNOWN")
                score = self.safe_float(r.get("score"))
            else:
                asset_name, score = str(r), 0.0
            
            table.add_row(str(i + 1), asset_name.upper(), f"{score:.4f}")
        return table

    def run(self):
        try:
            snapshot = self.engine.snapshot()
            data = snapshot.get("data", {})
            
            # 1. Prepare clean DataFrame for models
            df = pd.DataFrame.from_dict(data, orient="index")
            # Ensure price/change are floats for math operations
            for col in ['price', 'change']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)
            
            # 2. Macro Logic
            macro_model = MacroFactorModel(df)
            # Try to get regime, fallback to 'NEUTRAL' if unknown
            macro_regime = "UNKNOWN"
            for method in ["detect_regime", "macro_regime_signal"]:
                if hasattr(macro_model, method):
                    res = getattr(macro_model, method)()
                    if res: macro_regime = str(res).upper()

            # 3. Energy Logic
            energy_model = EnergyShockModel(df)
            energy_signal = energy_model.macro_energy_signal() if hasattr(energy_model, "macro_energy_signal") else "N/A"

            # 4. AI Ranking Logic
            ai_model = AIRankingModel(df)
            rankings = ai_model.rank_assets()

            # Fix: If rankings are empty or just column names, generate them from data
            valid_rankings = []
            if rankings:
                for r in rankings:
                    name = r.get("asset", "") if isinstance(r, dict) else str(r)
                    if name.lower() not in ['asset', 'price', 'change', 'ticker']:
                        valid_rankings.append(r)

            if not valid_rankings:
                # Fallback: Rank by absolute performance if AI model fails
                top_df = df.sort_values(by="change", ascending=False)
                valid_rankings = [{"asset": idx, "score": row["change"]} for idx, row in top_df.head(5).iterrows()]

            # 5. Render
            header = Panel(f"GLOBAL MACRO AI TERMINAL PRO\n{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", style="bold blue")
            self.console.print(header)
            self.console.print(self.build_market_table(data))
            self.console.print(Panel(f"REGIME: [bold yellow]{macro_regime}[/]\nENERGY: [bold cyan]{energy_signal}[/]", title="MACRO INTELLIGENCE"))
            self.console.print(self.build_ai_ranking_table(valid_rankings))

        except Exception as e:
            self.console.print(f"[bold red]TERMINAL ERROR[/bold red]\n{str(e)}")
