# Import packages
from dash import Dash, html
import dash_bootstrap_components as dbc


from portfolio import Portfolio

pf = Portfolio(db_name="fake_data.sqlite3")

percentage_profit = pf.get_profit_percentage()
positive_percent = percentage_profit > 0

total_portfolio_value = pf.get_total_value()

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN, "assets/style.css"]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container(
    [
        html.Div(
            [
                html.Small("Total Balance", className="mx-3"),
                html.H4(
                    [
                        f"$ {total_portfolio_value} ",
                        html.Small(
                            f"{'+' if positive_percent else ''}{percentage_profit} %",
                            style={
                                "color": "green" if positive_percent else "red",
                                "border": "0.5px solid black",
                                "borderRadius": "5px",
                                "padding": "3px",
                                "fontSize": "0.6em",
                                "marginLeft": "15px",
                            },
                        ),
                    ],
                    className="mx-3",
                ),
            ],
            className="mx-auto my-5 py-5 main-div",
            style={
                "backgroundColor": "#f8f9fa",
                "borderRadius": "10px",
            },
        ),
    ],
    fluid=True,
)


# Run the app
if __name__ == "__main__":
    app.run(debug=True)
