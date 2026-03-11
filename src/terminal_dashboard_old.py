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

        # Handle various return types from the AI model
        for i, r in enumerate(rankings):
            if isinstance(r, dict):
                asset_name = r.get("asset", "UNKNOWN")
                score = self.safe_float(r.get("score"))
                rank = r.get("rank", i + 1)
            elif isinstance(r, (list, tuple)) and len(r) >= 2:
                # Handle (asset, score) tuples
                asset_name, score = r[0], r[1]
                rank = i + 1
            else:
                # Fallback for strings
                asset_name = str(r)
                score = 0.0
                rank = i + 1
            
            # Filter out internal column names that might have leaked into rankings
            if asset_name.lower() in ['asset', 'price', 'change', 'ticker', 'ai_score']:
                continue

            table.add_row(str(rank), asset_name.upper(), f"{score:.4f}")

        return table

    def get_macro_regime(self, model):
        # Try different common method names for macro models
        for method in ["detect_regime", "macro_regime_signal", "get_regime"]:
            if hasattr(model, method):
                res = getattr(model, method)()
                if res: return str(res).upper()
        return "UNKNOWN"

    def run(self):
        try:
            snapshot = self.engine.snapshot()
            data = snapshot.get("data", {})
            if not data:
                raise ValueError("No data received from MarketDataEngine")

            # Convert to DataFrame
            df = pd.DataFrame.from_dict(data, orient="index")
            df.index.name = 'asset'
            df = df.reset_index()

            # Ensure numeric columns are actually numeric for the models
            for col in ['price', 'change']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

            # Initialize Models
            macro_model = MacroFactorModel(df)
            macro_regime = self.get_macro_regime(macro_model)

            energy_model = EnergyShockModel(df)
            energy_signal = "N/A"
            if hasattr(energy_model, "macro_energy_signal"):
                energy_signal = energy_model.macro_energy_signal()

            ai_model = AIRankingModel(df)
            rankings = ai_model.rank_assets()

            # UI components
            header = Panel(f"GLOBAL MACRO AI TERMINAL PRO\n{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC", style="bold blue")
            market_table = self.build_market_table(data)
            macro_panel = Panel(f"REGIME: [bold yellow]{macro_regime}[/]\nENERGY: [bold cyan]{energy_signal}[/]", title="MACRO INTELLIGENCE")
            ranking_table = self.build_ai_ranking_table(rankings)

            self.console.print(header)
            self.console.print(market_table)
            self.console.print(macro_panel)
            self.console.print(ranking_table)

        except Exception as e:
            self.console.print(f"[bold red]TERMINAL ERROR[/bold red]\n{str(e)}")
