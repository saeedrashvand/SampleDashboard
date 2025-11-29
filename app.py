# app.py
import os
import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# دیتا نمونه
data = {
    "Date": pd.date_range(start="2024-01-01", periods=100),
    "Region": ["Tehran", "Isfahan", "Tabriz", "Shiraz"] * 25,
    "Sales": [x * 10 for x in range(1, 101)],
    "Product": ["A", "B", "C", "D"] * 25
}
df = pd.DataFrame(data)

app = Dash(__name__)
server = app.server  # مهم: gunicorn از این استفاده می‌کند

app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "maxWidth": "1000px", "margin": "auto"}, children=[
    html.H1("داشبورد فروش", style={"textAlign": "center"}),
    html.Div([
        html.Div([
            html.Label("محصول:"),
            dcc.Dropdown(
                id="product_filter",
                options=[{"label": p, "value": p} for p in sorted(df["Product"].unique())],
                value="A",
                clearable=False,
                style={"width": "200px"}
            )
        ], style={"display": "inline-block", "marginRight": "20px"}),

        html.Div(id="kpis", style={"display": "inline-block", "verticalAlign": "top"})
    ], style={"marginBottom": "20px"}),

    dcc.Graph(id="sales_chart"),

    html.H4("Top Regions"),
    dcc.Graph(id="top_regions")
])

@app.callback(
    Output("sales_chart", "figure"),
    Output("kpis", "children"),
    Output("top_regions", "figure"),
    Input("product_filter", "value")
)
def update(product):
    filtered = df[df["Product"] == product]
    fig1 = px.line(filtered, x="Date", y="Sales", title=f"روند فروش محصول {product}")

    total = filtered["Sales"].sum()
    avg = filtered["Sales"].mean()

    kpi_div = html.Div([
        html.Div([html.H3(f"{total:,}"), html.P("جمع فروش")], style={"display":"inline-block", "marginRight":"30px"}),
        html.Div([html.H3(f"{avg:.2f}"), html.P("میانگین روزانه")], style={"display":"inline-block"})
    ])

    top = filtered.groupby("Region")["Sales"].sum().reset_index().sort_values("Sales", ascending=False)
    fig2 = px.bar(top, x="Region", y="Sales", title="مناطق برتر")

    return fig1, kpi_div, fig2

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=False)
