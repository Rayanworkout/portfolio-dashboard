import plotly.graph_objs as go
from plotly.offline import plot


def create_plot():
    dates = ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
    portfolio_values = [10000, 10500, 10200, 10800, 11000]

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
