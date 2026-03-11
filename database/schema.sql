-- Global Macro AI Terminal Pro - Database Schema

-- 1. Market Snapshots (Stores price, change, and metadata)
CREATE TABLE IF NOT EXISTS market_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset TEXT NOT NULL,
    ticker TEXT NOT NULL,
    price REAL NOT NULL,
    change_pct REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Macro Signals (Stores detected regimes like 'ENERGY SHOCK')
CREATE TABLE IF NOT EXISTS macro_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    regime TEXT NOT NULL,
    energy_signal TEXT,
    vix_level REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 3. AI Rankings (Stores the final ranked output)
CREATE TABLE IF NOT EXISTS ai_rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rank INTEGER NOT NULL,
    asset TEXT NOT NULL,
    score REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indices for faster lookup during analysis
CREATE INDEX IF NOT EXISTS idx_market_asset ON market_snapshots(asset);
CREATE INDEX IF NOT EXISTS idx_market_time ON market_snapshots(timestamp);
CREATE INDEX IF NOT EXISTS idx_macro_time ON macro_signals(timestamp);
