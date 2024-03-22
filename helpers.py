import plotly.graph_objs as go
from plotly.offline import plot

from portfolio import Portfolio

def generate_pf_plot():

    pf = Portfolio(name="main", db_name="portfolio/portfolio.sqlite3")

    data = pf.get_value_history()

    data = [(k, v) for k, v in data["value"].items()]

    dates = [d[0] for d in data]
    portfolio_values = [d[1] for d in data]

    # Create Plotly trace
    trace = go.Scatter(
        x=dates, y=portfolio_values, mode="lines+markers", name="Portfolio Value"
    )

    # Create Plotly layout
    layout = go.Layout(
        title="Portfolio Value Over Time",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Portfolio Value"),
    )

    # Create Plotly figure
    fig = go.Figure(data=[trace], layout=layout)

    # Plot the figure and save it as a div
    chart_div = plot(fig, output_type="div")

    return chart_div


if __name__ == "__main__":
    generate_pf_plot()
