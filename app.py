import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px

# 1. Load the data
df = pd.read_csv("formatted_sales_data.csv")

# 2. Clean column names and data
df.columns = df.columns.str.strip()
df['date'] = pd.to_datetime(df['date'])
# Region names ko lowercase kar dena behtar hai comparison ke liye
df['region'] = df['region'].str.strip().str.lower()
df = df.sort_values(by="date")

# 3. Initialize Dash
app = Dash(__name__)

# 4. App Layout (Cute Professional Theme)
app.layout = html.Div(style={
    'backgroundColor': '#FFD1DC',
    'padding': '50px',
    'fontFamily': 'Arial, sans-serif',
    'minHeight': '100vh'
}, children=[

    html.Div(style={
        'textAlign': 'center',
        'padding': '20px',
        'backgroundColor': 'rgba(255, 255, 255, 0.5)',
        'borderRadius': '15px',
        'marginBottom': '30px'
    }, children=[
        html.H1('🌸 Pink Morsel Sales Visualiser 🌸', style={'color': '#2c3e50'}),
    ]),

    html.Div(style={
        'textAlign': 'center',
        'marginBottom': '40px',
        'padding': '15px',
        'backgroundColor': 'white',
        'borderRadius': '50px',
        'boxShadow': '0 4px 10px rgba(0,0,0,0.05)'
    }, children=[
        html.Label("Select Region: ", style={'fontWeight': 'bold', 'marginRight': '15px'}),
        dcc.RadioItems(
            id='region-picker',
            options=[
                {'label': 'North', 'value': 'north'},
                {'label': 'East', 'value': 'east'},
                {'label': 'South', 'value': 'south'},
                {'label': 'West', 'value': 'west'},
                {'label': 'All', 'value': 'all'}
            ],
            value='all',
            inline=True,
            labelStyle={'marginRight': '15px'}
        ),
    ]),

    html.Div(style={
        'backgroundColor': 'white',
        'padding': '20px',
        'borderRadius': '20px',
        'boxShadow': '0px 8px 20px rgba(0,0,0,0.1)'
    }, children=[
        dcc.Graph(id='sales-line-chart')
    ])
])


# 5. Callback with Error Handling Fix
@callback(
    Output('sales-line-chart', 'figure'),
    Input('region-picker', 'value')
)
def update_graph(selected_region):
    # Filter data based on selection
    if selected_region == 'all':
        filtered_df = df
    else:
        # Ensure comparison is case-insensitive
        filtered_df = df[df['region'] == selected_region.lower()]

    # Create figure
    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title=f"Sales Analysis: {selected_region.upper()}",
        template="plotly_white"
    )

    # Styling the line to Black
    fig.update_traces(line=dict(color='black', width=2))

    return fig


if __name__ == '__main__':
    app.run(debug=True)