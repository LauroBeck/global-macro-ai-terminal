import sqlite3
import os
from rich.console import Console
from rich.table import Table

def view_macro_history():
    console = Console()
    # Lock to the Current Working Directory where you just saw the file with 'ls'
    db_path = os.path.join(os.getcwd(), "macro_terminal.db")
    
    if not os.path.exists(db_path):
        console.print(f"[red]Database file not found at: {db_path}[/red]")
        return

    try:
        # Use a context manager to ensure the file handle is released
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT timestamp, regime, energy_signal FROM macro_signals ORDER BY timestamp DESC LIMIT 10")
            rows = cursor.fetchall()
            
            if not rows:
                console.print("[yellow]The database file exists, but the 'macro_signals' table is empty.[/yellow]")
                console.print("[dim]Ensure the dashboard is calling self.db.save_snapshot() inside its loop.[/dim]")
                return

            table = Table(title="🏛️ Macro Regime History")
            table.add_column("Timestamp", style="cyan")
            table.add_column("Regime", style="bold magenta")
            table.add_column("Energy Detail", style="green")

            for row in rows:
                table.add_row(str(row[0]), str(row[1]), str(row[2]))

            console.print(table)
            
    except Exception as e:
        console.print(f"[red]Error reading database: {e}[/red]")

if __name__ == "__main__":
    view_macro_history()
