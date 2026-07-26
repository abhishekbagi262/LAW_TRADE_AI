# EXP-001: Entry Logic Experiment

Date: 2026-07-26
Branch: experiment/entry-logic

## Baseline

Current entry condition:
- Bullish SMA20/SMA50 crossover
- MACD bullish confirmation
- RSI between 50 and 70

## Baseline True Walk-Forward Results

RELIANCE.NS: 1.60%
TCS.NS: 1.54%
HDFCBANK.NS: 0.00%
INFY.NS: 3.56%
ITC.NS: 0.00%

Total testing windows: 25

## Problem

The strategy produces very few trades.
HDFCBANK.NS and ITC.NS produced zero trades in all five testing windows.

## Goal

Test whether the entry logic is too restrictive while preserving risk management.

## Experiment Status

PENDING
