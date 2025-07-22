import pandas as pd
import yfinance as yf
import xlsxwriter
from utils.data_loader import load_yahoo_finance_prices
import logging

def export_results_to_excel(nav_series, portfolio_details, start_date, end_date, output_path="output/backtest_with_chart.xlsx"):
    """
    Exports NAV and S&P500 benchmark to Excel with an embedded chart.

    Args:
        nav_series (pd.Series): Portfolio NAV indexed by date.
        start_date (str): Start date for benchmark (YYYY-MM-DD).
        end_date (str): End date for benchmark (YYYY-MM-DD).
        output_path (str): Output Excel file path.
    """
    # Fetch S&P 500 data (Adj Close)
    sp500 = load_yahoo_finance_prices(["^GSPC"], start_date, end_date)
    sp500 = sp500 / sp500.iloc[0] * nav_series.iloc[0]  # Rebase to NAV start
    cols = list(sp500.columns)
    sp500 = sp500[cols[0]]
    # Combine into a DataFrame
    df = pd.concat([nav_series.rename("NAV"), sp500.rename("S&P 500")], axis=1)
    df = df.dropna()

    # Create Excel file
    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        # Write Performance sheet
        df.to_excel(writer, sheet_name="Performance")
        workbook = writer.book
        worksheet_perf = writer.sheets["Performance"]

        # Create chart for Performance
        chart = workbook.add_chart({"type": "line"})
        chart.add_series({
            "name": "NAV",
            "categories": f"=Performance!$A$2:$A${len(df)+1}",
            "values": f"=Performance!$B$2:$B${len(df)+1}",
        })
        chart.add_series({
            "name": "S&P 500",
            "categories": f"=Performance!$A$2:$A${len(df)+1}",
            "values": f"=Performance!$C$2:$C${len(df)+1}",
        })
        chart.set_title({"name": "Portfolio NAV vs S&P 500"})
        chart.set_x_axis({"name": "Date"})
        chart.set_y_axis({"name": "Value"})
        worksheet_perf.insert_chart("E2", chart)

        # Write Portfolio Constituents sheet
        portfolio_details.to_excel(writer, sheet_name="Portfolio_Constituents", index=False)


    logging.info(f"Excel file created: {output_path}")
    