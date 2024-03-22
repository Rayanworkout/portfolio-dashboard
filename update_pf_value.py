import time

from portfolio import Portfolio

def update_pf_value() -> None:
    """
    Function to update the portfolio value every 24 hours.
    The data is used to create a chart.

    """
    while True:
        pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

        current_value = pf.get_total_value()

        pf.db.insert_current_value_for_chart(current_value)

        print(f"Updated portfolio value: {current_value}")

        # time.sleep(86400)  # Sleep for 24 hours
        time.sleep(30)