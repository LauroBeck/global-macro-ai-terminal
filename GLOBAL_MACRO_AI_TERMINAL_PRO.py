#!/usr/bin/env python3
import sys
import os

# Add the current directory to path so it can find the src folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.terminal_dashboard import TerminalDashboard

def main():
    """
    Main entry point for the Global Macro AI Terminal.
    """
    try:
        # Initialize the dashboard
        dashboard = TerminalDashboard()
        
        # Run the dashboard
        dashboard.run()
        
    except KeyboardInterrupt:
        print("\n[!] Terminal closed by user.")
        sys.exit(0)
    except Exception as e:
        print(f"[-] A critical error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
