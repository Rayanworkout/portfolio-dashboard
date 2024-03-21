from flask import Flask, render_template

from helpers import create_plot
from portfolio import Portfolio


app = Flask(__name__)


@app.route("/")
def index():

    pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

    data = {
        "total_value": pf.get_total_value(),
        "total_profit": pf.get_profit(),
        "total_profit_percentage": pf.get_profit(percentage=True),
        "tokens_with_holdings": pf.get_all_tokens_with_their_value_and_holdings(),
    }

    # chart_div = create_plot()

    return render_template("index-page.html", portfolio=data)


# flask --app app run --debug
