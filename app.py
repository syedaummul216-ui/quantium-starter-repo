import pandas as pd
from dash import Dash, html, dcc
import plotly.express as px

# 1. Load the data
df = pd.read_csv("formatted_sales_data.csv")

# 2. Fix spaces in column names
df.columns = df.columns.str.strip()

# 3. FIXED: Convert 'date' string to actual Datetime objects
# Is se dates 1/1/2019 ke baad 1/2/2019 aayengi, alphabet order mein nahi
df['date'] = pd.to_datetime(df['date'])

# 4. Sort by date properly
df = df.sort_values(by="date")

# 5. Initialize Dash
app = Dash(__name__)

# 6. Create Chart
# 'render_mode' ko 'svg' rakha hai taake line mazeed saaf nazar aaye
line_chart = px.line(
    df,
    x="date",
    y="sales",
    title="Pink Morsel Sales Analysis (Over Time)",
    labels={"date": "Date", "sales": "Sales (USD)"},
    template="plotly_white"
)

# 7. Layout
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    html.H1(
        children='Soul Foods: Pink Morsel Visualiser',
        style={'textAlign': 'center', 'color': '#2c3e50'}
    ),

    html.P(
        children="Analysis of sales before and after the price increase on January 15, 2021.",
        style={'textAlign': 'center', 'color': '#7f8c8d'}
    ),

    dcc.Graph(
        id='sales-line-chart',
        figure=line_chart
    )
])

# 8. Run the app
if __name__ == '__main__':
    app.run(debug=True)