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

            table.add_row(
                str(asset), 
                ticker, 
                f"{price:.2f}", 
                f"[{color}]{change:.2f}%[/{color}]"
            )
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

    def get_macro_regime(self, model):
        # We must check for 'market_regime' to match your model's code
        for method in ["market_regime", "detect_regime", "macro_regime_signal"]:
            if hasattr(model, method):
                res = getattr(model, method)()
                if res: 
                    return str(res).upper()
        return "UNKNOWN"

    def run(self):
        try:
            snapshot = self.engine.snapshot()
            data = snapshot.get("data", {})

            # 1. Create DataFrame and FIX the 'asset' column issue
            df = pd.DataFrame.from_dict(data, orient="index")
            df.index.name = 'asset'
            df = df.reset_index()

            # 2. Force numeric types for model calculations
            for col in ['price', 'change']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

            # 3. Initialize and run Models
            macro_model = MacroFactorModel(df)
            macro_regime = self.get_macro_regime(macro_model)

            energy_model = EnergyShockModel(df)
            energy_signal = "N/A"
            if hasattr(energy_model, "macro_energy_signal"):
                energy_signal = energy_model.macro_energy_signal()

            ai_model = AIRankingModel(df)
            rankings = ai_model.rank_assets()

            # 4. Filter out column names (asset, price, change) from rankings
            clean_rankings = []
            if isinstance(rankings, list):
                for item in rankings:
                    name = item.get("asset", "") if isinstance(item, dict) else str(item)
                    # Skip internal pandas names that leaked into the model
                    if str(name).lower() not in ['asset', 'price', 'change', 'ticker', 'index', 'ai_score']:
                        clean_rankings.append(item)

            # 5. Fallback: If AI rankings are empty/invalid, rank by performance
            if not clean_rankings:
                top_movers = df.sort_values(by="change", ascending=False).head(5)
                clean_rankings = [{"asset": row['asset'], "score": row['change']} for _, row in top_movers.iterrows()]

            # 6. UI Render
            header = Panel(
                f"GLOBAL MACRO AI TERMINAL PRO\n{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC",
                style="bold blue"
            )
            macro_panel = Panel(
                f"REGIME: [bold yellow]{macro_regime}[/]\nENERGY: [bold cyan]{energy_signal}[/]", 
                title="MACRO INTELLIGENCE"
            )

            self.console.print(header)
            self.console.print(self.build_market_table(data))
            self.console.print(macro_panel)
            self.console.print(self.build_ai_ranking_table(clean_rankings))

        except Exception as e:
            self.console.print(f"[bold red]TERMINAL ERROR[/bold red]\n{str(e)}")
