# DSP — NMP Research Lab

## Status
Internal research lab only. Not visible to users.

## Current production NMP
NMP v1:
- Momentum detector: RSI(7)
- Output: NMP Price Zone
- Reference: Open price of the opposite candle related to the momentum candle.

## Research purpose
Find the best detector for the reference candle that produces the strongest NMP price zone.

## Candidate momentum detectors
- RSI(7)
- RSI(14)
- RSI(21)
- ROC(5)
- ROC(10)
- ROC(14)
- Momentum(5)
- Momentum(10)
- Momentum(14)
- MACD Histogram
- CCI
- Stochastic
- Price Momentum
- ATR Adjusted Price Momentum

## Candidate reference prices
For the opposite candle:
- Open
- Close
- Midpoint
- High
- Low

## Evaluation metrics
- NMP respect rate
- Bounce rate
- False break rate
- Distance from reversal point
- Support/resistance conversion
- Risk/reward usefulness
- Time validity

## Decision rule
The final NMP specification is not chosen by opinion.
It is chosen by historical test results across multiple assets and timeframes.
