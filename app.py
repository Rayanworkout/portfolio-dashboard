from flask import Flask, render_template, request, redirect, flash

from helpers import create_plot
from portfolio import Portfolio

import os
import dotenv

dotenv.load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")


@app.route("/")
def index():

    pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

    stablecoins = pf.get_stablecoins_value()

    data = {
        "total_value": pf.get_total_value(),
        "total_profit": pf.get_profit(),
        "total_profit_percentage": pf.get_profit(percentage=True),
        "stablecoins": stablecoins,
    }

    holdings = pf.get_all_tokens_with_their_value_and_holdings()

    # chart_div = create_plot()

    return render_template("index-page.html", portfolio=data, holdings=holdings)


@app.route("/new", methods=["GET", "POST"])
def new_transaction():
    if request.method == "POST":

        pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

        token = request.form["token"]
        qty = request.form["qty"]
        price = request.form["price"]
        fees = request.form["fees"]

        tx = {
            "qty": qty,
            "token": token,
            "cost": int(price) * float(qty),
            "fees": fees,
        }

        pf.db.add_transaction(tx)
        flash("Transaction added successfully!", "success")
        return redirect("/")

    return render_template("new-tx-page.html")


@app.route("token/<token>", methods=["GET", "POST"])
def token(token):
    pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

    token_value = pf.get_token_value(token)
    token_profit = pf.get_profit(token)
    token_profit_percentage = pf.get_profit(token, percentage=True)

    data = {
        "token": token,
        "token_value": token_value,
        "token_profit": token_profit,
        "token_profit_percentage": token_profit_percentage,
    }

    return render_template("token-page.html", token=data)


# flask --app app run --debug
