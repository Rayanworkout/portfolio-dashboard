import time

from portfolio import Portfolio


def update_pf_value(interval: int = 86400) -> None:
    """
    Function to update the portfolio value every 24 hours.
    The data is used to create a chart.

    """
    while True:
        pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

        current_value = pf.get_total_value()

        pf.db.insert_current_value_for_chart(current_value)

        print(f"Updated portfolio value: {current_value}")

        time.sleep(interval)


if __name__ == "__main__":
    update_pf_value(3600 * 24)
