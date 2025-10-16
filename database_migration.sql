-- Database Migration for Position Management System
-- Run this in your Supabase SQL Editor

-- Add new columns to open_trades table
ALTER TABLE open_trades 
ADD COLUMN IF NOT EXISTS position_size FLOAT DEFAULT 50.0,
ADD COLUMN IF NOT EXISTS leverage INTEGER DEFAULT 5,
ADD COLUMN IF NOT EXISTS pnl_usd FLOAT DEFAULT 0.0;

-- Add new columns to closed_trades table  
ALTER TABLE closed_trades
ADD COLUMN IF NOT EXISTS position_size FLOAT DEFAULT 50.0,
ADD COLUMN IF NOT EXISTS leverage INTEGER DEFAULT 5,
ADD COLUMN IF NOT EXISTS pnl_usd FLOAT DEFAULT 0.0;

-- Create portfolio_state table
CREATE TABLE IF NOT EXISTS portfolio_state (
    id SERIAL PRIMARY KEY,
    total_balance FLOAT NOT NULL DEFAULT 1000.0,
    available_balance FLOAT NOT NULL DEFAULT 1000.0,
    used_balance FLOAT NOT NULL DEFAULT 0.0,
    total_pnl FLOAT NOT NULL DEFAULT 0.0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert initial portfolio state
INSERT INTO portfolio_state (total_balance, available_balance, used_balance, total_pnl)
VALUES (1000.0, 1000.0, 0.0, 0.0)
ON CONFLICT DO NOTHING;

-- Update existing trades with default values
UPDATE open_trades 
SET position_size = 50.0, leverage = 5, pnl_usd = 0.0 
WHERE position_size IS NULL;

UPDATE closed_trades 
SET position_size = 50.0, leverage = 5, pnl_usd = 0.0 
WHERE position_size IS NULL;
