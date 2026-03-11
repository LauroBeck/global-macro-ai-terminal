# config/tickers.py

TECH_STOCKS = {
    "IBM": "IBM",
    "ORACLE": "ORCL",
    "MICROSOFT": "MSFT",
    "NVIDIA": "NVDA"
}

ENERGY_STOCKS = {
    "CHEVRON": "CVX",
    "EXXON": "XOM",
    "BP": "BP",
    "SHELL": "SHEL",
    "CONOCOPHILLIPS": "COP"
}

MACRO_INDEXES = {
    "NASDAQ": "^IXIC",
    "SP500_FUTURES": "ES=F",
    "VIX": "^VIX"
}

COMMODITIES = {
    "OIL": "CL=F",
    "GOLD": "GC=F"
}

TREASURY = {
    "US10Y": "^TNX"
}

ALL_TICKERS = {
    **TECH_STOCKS,
    **ENERGY_STOCKS,
    **MACRO_INDEXES,
    **COMMODITIES,
    **TREASURY
}
