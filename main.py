import pandas as pd
from backtest import backtest_qvm_strategy
from utils.data_loader import load_fundamentals
from utils.plotting import export_results_to_excel
import os
import random
import logging

LOG_FILE = os.path.join("output", "backtest_logs.txt")
os.makedirs("output", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode='w'),  # overwrite each run
        logging.StreamHandler()                   # also print to console
    ]
)

rand_id = random.randint(1000, 9999)

# Paths
DATA_FILE = "data/aristocrats_pe.xlsx"
OUTPUT_FILE = f"backtest_results_{rand_id}.xlsx"
OUTPUT_NAV = f"output/{OUTPUT_FILE}"
start_date = "2023-01-31"
end_date = "2023-07-31"
reblancing_frequency = "6ME"

def main():
    # 1. Load fundamentals (aristocrats + PE ratios)
    fundamentals = load_fundamentals(DATA_FILE)

    # 2. Run backtest
    nav_series, portfolio_details = backtest_qvm_strategy(
        fundamentals=fundamentals,
        start_date=start_date,
        end_date=end_date,
        rebalance_freq=reblancing_frequency,
        top_n=25,
        max_pe=20,
        max_per_sector=5
    )

    # 3. Save results
    export_results_to_excel(nav_series, portfolio_details, start_date, end_date, OUTPUT_NAV)
    logging.info(f"Backtest complete. Results saved to {OUTPUT_NAV}.")

    if os.path.exists(OUTPUT_NAV):
        try:
            os.startfile(os.path.join("output", OUTPUT_FILE))
            logging.info(f"Opened file: {OUTPUT_NAV}")
        except Exception as e:
            logging.info(f"Could not open file automatically: {e}")

if __name__ == "__main__":
    main()
