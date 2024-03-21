from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    percent = 50
    gains = 100
    return render_template("index.html", percent=percent, gains=gains)
