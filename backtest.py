import pandas as pd
from utils.data_loader import load_yahoo_finance_prices
import yfinance as yf
from collections import defaultdict
import logging


def get_sector(ticker):
    """
    Fetch sector information using yfinance.
    Consider caching results for performance.
    """
    try:
        stock = yf.Ticker(ticker.split()[0])
        return stock.info.get("sector", "Unknown")
    except Exception:
        return "Unknown"

def select_top_25_with_constraints(candidates, top_n=25, max_per_sector=5):
    """
    Select top 25 stocks by PE, respecting sector diversification (<=5 per sector).
    candidates: List of tuples (ticker, PE).
    Returns: List of selected tickers.
    """
    sorted_candidates = sorted(candidates, key=lambda x: x[1])
    selected = []
    sector_count = defaultdict(int)

    for ticker, pe in sorted_candidates:
        sector = get_sector(ticker)
        if sector_count[sector] < max_per_sector:
            selected.append(ticker)
            sector_count[sector] += 1
        if len(selected) == top_n:
            break

    return selected

def backtest_qvm_strategy(fundamentals, start_date, end_date,
                      rebalance_freq='6ME', top_n=25, max_pe=20, max_per_sector=5):
    """
    Backtest a Dividend Aristocrat strategy with PE filtering,
    equal weighting, sector constraints, and carry-forward logic.

    Returns:
        nav_series (pd.Series)
        portfolio_details (pd.DataFrame)
    """
    rebal_dates = pd.date_range(start=start_date, end=end_date, freq=rebalance_freq)
    if rebal_dates[-1] != pd.to_datetime(end_date):
        rebal_dates = rebal_dates.append(pd.DatetimeIndex([end_date]))
    nav_series = pd.Series([100], index=[rebal_dates[0]])  # Start NAV at 100
    portfolio_value = 100
    portfolio_records = []

    current_tickers = []  # Track current portfolio

    for i in range(len(rebal_dates) - 1):
        date = rebal_dates[i]
        next_date = rebal_dates[i + 1]

        # Filter candidates by PE
        candidates = [(ticker, pe_values.get(date))
                      for ticker, pe_values in fundamentals.items()
                      if date in pe_values and pe_values[date] <= max_pe]

        if len(candidates) >= top_n:
            # Select new portfolio with constraints
            selected_tickers = select_top_25_with_constraints(candidates, top_n, max_per_sector)
            current_tickers = selected_tickers
        elif not current_tickers:
            # No previous portfolio and no candidates
            logging.info(f"Skipping {date.date()} – No candidates and no previous portfolio.")
            continue
        else:
            # Carry forward previous portfolio
            selected_tickers = current_tickers
            logging.info(f"Carrying forward portfolio from {date.date()}.")

        # Equal weights
        n = len(selected_tickers)
        weights = {t: 1 / n for t in selected_tickers}

        # Load price data
        price_slice = load_yahoo_finance_prices(selected_tickers, date, next_date)
        if price_slice.empty or price_slice.shape[0] < 2:
            continue

        # Calculate NAV
        start_prices = price_slice.iloc[0]
        returns = price_slice.divide(start_prices)
        weighted_nav = returns.mul(pd.Series(weights)).sum(axis=1) * portfolio_value
        nav_series = pd.concat([nav_series, weighted_nav[1:]])
        portfolio_value = weighted_nav.iloc[-1]

        # Record constituents
        for t in selected_tickers:
            portfolio_records.append({
                "Date": date,
                "Ticker": t,
                "Weight": weights[t],
                "Sector": get_sector(t)
            })

    portfolio_details = pd.DataFrame(portfolio_records)
    return nav_series, portfolio_details