import dotenv
import os

from flask import Flask, render_template, request, redirect, flash, url_for

from helpers import generate_pf_plot
from portfolio import Portfolio


dotenv.load_dotenv()


app = Flask(__name__)

app.secret_key = os.getenv("FLASK_SECRET_KEY")


all_cgecko_tokens = Portfolio.get_all_cgecko_tokens()


@app.route("/")
def index():

    pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

    stablecoins = pf.get_stablecoins_value()

    total_value = pf.get_total_value()

    data = {
        "total_value": total_value,
        "total_profit": pf.get_profit(total_value=total_value),
        "total_profit_percentage": pf.get_profit(
            percentage=True, total_value=total_value
        ),
        "stablecoins": stablecoins,
    }

    holdings = pf.get_all_tokens_with_their_value_and_holdings()

    chart_div = generate_pf_plot()

    return render_template(
        "index-page.html", portfolio=data, holdings=holdings, chart=chart_div
    )


@app.route("/new", methods=["GET", "POST"])
def new_transaction():
    if request.method == "POST":

        pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

        token = request.form["token"]
        qty = request.form["qty"]
        price = request.form["price"]
        fees = request.form["fees"]

        # Values checks
        if not qty or not price or not fees:
            flash("Please fill all the fields", "danger")
            return redirect("/new")

        if token not in all_cgecko_tokens:
            flash("Token not found", "danger")
            return redirect("/new")

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


@app.route("/token/<string:token>")
def token_page(token):
    pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

    token_value = pf.get_token_value(token)
    token_profit = pf.get_profit(token)
    token_profit_percentage = pf.get_profit(token, percentage=True)

    token_transactions = pf.get_token_transactions(token)

    data = {
        "token": token,
        "value": token_value,
        "profit": token_profit,
        "profit_percentage": token_profit_percentage,
        "transactions": token_transactions,
    }

    return render_template("token-page.html", token=data)


@app.route("/delete/<string:token>/<int:tx_id>")
def delete_transaction(token, tx_id):
    pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")
    pf.db.delete_transaction(tx_id)
    return redirect(url_for("token_page", token=token))


# flask --app app run --debug
