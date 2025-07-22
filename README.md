# Dividend Aristocrat Backtest

## Overview
This project implements a **backtesting framework** for a Dividend Aristocrat strategy with the following constraints:
- **Equal Weighting:** Each of the 25 selected stocks gets an equal weight of 4%.
- **Sector Diversification:** No more than 20% of the portfolio (5 stocks) comes from a single sector.
- **Semi-Annual Rebalancing:** The portfolio is rebalanced every 6 months based on updated PE ratios.

The script outputs:
1. **Performance sheet (Excel):** NAV of the strategy vs. the S&P 500 benchmark.
2. **Portfolio Constituents sheet (Excel):** Shows tickers, weights, and sectors for each rebalancing date.
3. **Log file:** Tracks all steps and warnings from the backtest.

---

## Project Structure
```
project/
│
├── main.py                 # Entry point for running the backtest
├── backtest.py             # Core backtest logic (portfolio construction, NAV calc)
├── utils/
│   ├── data_loader.py      # Load PE/fundamentals and price data
│   └── plotting.py         # Exports performance & portfolio details to Excel
├── data/
│   └── aristocrats_pe.xlsx # Input: Dividend Aristocrats with PE ratios history
├── output/
│   ├── backtest_results_xxxx.xlsx # Output Excel file with results
│   └── backtest_logs.txt   # Log file with detailed backtest events
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

---

## Requirements
- **Python 3.11.7+**
- Install dependencies:
  ```bash
  pip install -r requirements.txt
  ```

---

## How to Run
1. Place your input file `aristocrats_pe.xlsx` in the `data/` folder.
2. Run the main script:
   ```bash
   python main.py
   ```
3. Results will be saved in the `output/` folder:
   - `backtest_results_<random_id>.xlsx`
   - `backtest_logs.txt`
4. The Excel file will automatically open upon completion.

---

## Notes
- Price data is fetched via Yahoo Finance.
- Sector information is retrieved via `yfinance` (internet connection required).
- The script enforces portfolio constraints as requested.

---

## Contact
For questions or improvements, please contact the developer.
