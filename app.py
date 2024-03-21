from flask import Flask, render_template
from helpers import create_plot

app = Flask(__name__)


@app.route("/")
def index():
    percent = 50
    gains = 100
    pnl = 0

    # <p>Ethereum</p>
    # <p>1.6</p>
    # <p>$1540</p>
    # <p>25%</p>

    all_tokens = [
        {
            "name": "ETH",
            "balance": 1.6,
            "value": 1540,
            "roi": 25,
        },
        {
            "name": "BTC",
            "balance": 0.5,
            "value": 6000,
            "roi": 10,
        },
        {
            "name": "DOGE",
            "balance": 1000,
            "value": 0.3,
            "roi": 5,
        },
    ]

    # chart_div = create_plot()

    return render_template(
        "index-page.html", percent=percent, gains=gains, pnl=pnl, tokens=all_tokens
    )
