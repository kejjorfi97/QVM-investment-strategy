import yfinance as yf
import pandas as pd
from collections import defaultdict

def load_yahoo_finance_prices(tickers, start_date, end_date):
    try:
        """
        Fetches historical adjusted close prices for a list of tickers from Yahoo Finance.
        """
        data = yf.download(tickers, start=start_date, end=end_date)
        if isinstance(data, pd.Series):
            data = data.to_frame()
        data = data[[('Close', ticker) for ticker in tickers]]
        data.columns = data.columns.droplevel()
        missing_prices=[]
        for col in data.columns:
            d=data[col].drop_duplicates()
            if len(d) == 1:
                missing_prices.append(col)
        assert len(missing_prices) == 0, f"No prices found for these tickers: {', '.join(missing_prices)}"
        data = data.dropna()
        return data.dropna()
    except Exception as e:
        print(str(e))
        return pd.DataFrame()
    
def load_fundamentals(file_path: str) -> dict:
    """
    Load aristocrats + PE ratios from an Excel file into a nested dict.
    
    Excel format expected:
    Ticker | Date        | PE
    ------ | ----------- | -----
    AXP | 2020-01-31  | 15.85
    AXP | 2020-07-31  | 19.40
    ...

    Returns:
        fundamentals (dict): {ticker: {date: PE}}
    """
    # Read the Excel file
    df = pd.read_excel(file_path)

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'])

    # Strip spaces in Ticker column
    df['Ticker'] = df['Ticker'].str.strip()

    # Build the nested dict
    fundamentals = defaultdict(dict)
    for _, row in df.iterrows():
        ticker = row['Ticker']
        date = row['Date']
        pe = row['PE']
        if pd.notna(pe):
            fundamentals[ticker][date] = float(pe)

    return dict(fundamentals)
