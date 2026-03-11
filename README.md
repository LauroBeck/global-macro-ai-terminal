# 🏛️ Global Macro AI Terminal Pro

A professional-grade terminal dashboard for real-time global market analysis, regime detection, and AI-driven asset ranking. 

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Live-orange.svg)

## 🎯 Overview
The **Global Macro AI Terminal Pro** is a lightweight, CLI-based financial workstation. It aggregates multi-asset market data and runs it through specialized quant models to detect economic regimes and rank assets based on AI scoring.

### Key Features
* **Real-Time Market Snapshot:** Tracks Equities (NVDA, MSFT), Commodities (Gold, Oil), and Volatility (VIX).
* **Macro Intelligence Engine:** Automated detection of market regimes such as `ENERGY SHOCK`, `SAFE HAVEN FLOW`, and `RISK ON`.
* **AI Asset Ranking:** Proprietary scoring model that filters market noise to find the top 5 high-conviction assets.
* **Auto-Refresh Desk:** Live-ticking interface with UTC synchronization for professional monitoring.

---

## 🛠️ Technical Stack
* **Language:** Python 3.10+
* **UI Framework:** `Rich` (Terminal formatting and tables)
* **Data Processing:** `Pandas` & `NumPy`
* **Models:** Specialized Factor Analysis and Energy Shock Models

---

## 🚀 Getting Started

### Prerequisites
Ensure you have Python installed, then install the required dependencies:
```bash
pip install -r requirements.txt

Installation

    Clone the repository:
    Bash

    git clone [https://github.com/YOUR_USERNAME/global-macro-ai-terminal.git](https://github.com/YOUR_USERNAME/global-macro-ai-terminal.git)
    cd global-macro-ai-terminal

    Run the terminal:
    Bash

    python3 GLOBAL_MACRO_AI_TERMINAL_PRO.py

📊 Model Logic
🔍 Macro Regime Detection

The terminal analyzes the inter-market relationship between OIL, GOLD, and VIX:

    Energy Shock: Triggered if Oil volatility exceeds ±5%.

    Volatility Stress: Triggered if VIX exceeds 25.00.

    Safe Haven Flow: Detected when Gold rallies while the Nasdaq shows weakness.

🤖 AI Ranking Model

Assets are ranked using a multi-factor approach that excludes technical headers and focuses purely on high-performance tickers.
📂 Project Structure
Plaintext

├── src/
│   ├── terminal_dashboard.py   # UI and Logic Controller
│   ├── macro_factors.py        # Regime Detection Logic
│   ├── energy_shock_model.py   # Commodities Analysis
│   ├── ai_ranking_model.py     # Asset Scoring Engine
│   └── market_data_engine.py   # Data Feed Aggregator
├── GLOBAL_MACRO_AI_TERMINAL_PRO.py  # Main Entry Point
└── requirements.txt

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

Built for Quant-Research and Global Macro Strategy.
