import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objs as go

# Read the processed sales data
df = pd.read_csv('data/output.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values('date')

# Group by date and sum sales across all regions for the main trend line
daily_sales = df.groupby('date')['sales'].sum().reset_index()

# Create the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('Soul Foods - Pink Morsel Sales Analysis', 
                style={'textAlign': 'center', 'color': '#FF1493', 'marginBottom': '10px'}),
        html.H3('Sales Performance: Before vs After Price Increase (January 15, 2021)', 
                style={'textAlign': 'center', 'color': '#555', 'marginBottom': '30px'})
    ]),
    
    # Line chart
    dcc.Graph(
        id='sales-chart',
        figure={
            'data': [
                # Main sales line
                go.Scatter(
                    x=daily_sales['date'],
                    y=daily_sales['sales'],
                    mode='lines',
                    name='Total Daily Sales',
                    line=dict(color='#FF1493', width=2),
                    hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br>' +
                                  '<b>Sales</b>: $%{y:,.2f}<br>' +
                                  '<extra></extra>'
                )
            ],
            'layout': go.Layout(
                xaxis={
                    'title': 'Date',
                    'showgrid': True,
                    'gridcolor': '#E0E0E0'
                },
                yaxis={
                    'title': 'Total Daily Sales ($)',
                    'showgrid': True,
                    'gridcolor': '#E0E0E0'
                },
                hovermode='x unified',
                plot_bgcolor='#FAFAFA',
                paper_bgcolor='white',
                margin={'l': 60, 'r': 40, 't': 40, 'b': 60},
                # Add vertical line to mark the price increase date
                shapes=[
                    dict(
                        type='line',
                        x0='2021-01-15',
                        x1='2021-01-15',
                        y0=0,
                        y1=1,
                        yref='paper',
                        line=dict(
                            color='red',
                            width=2,
                            dash='dash'
                        )
                    )
                ],
                annotations=[
                    dict(
                        x='2021-01-15',
                        y=1,
                        yref='paper',
                        text='Price Increase<br>Jan 15, 2021',
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor='red',
                        ax=0,
                        ay=-40,
                        font=dict(color='red', size=12),
                        bgcolor='rgba(255, 255, 255, 0.8)',
                        bordercolor='red',
                        borderwidth=1
                    )
                ]
            )
        }
    ),
    
    # Regional breakdown
    html.Div([
        html.H3('Sales by Region', 
                style={'textAlign': 'center', 'color': '#555', 'marginTop': '40px', 'marginBottom': '20px'})
    ]),
    
    dcc.Graph(
        id='regional-sales-chart',
        figure={
            'data': [
                go.Scatter(
                    x=df[df['region'] == region]['date'],
                    y=df[df['region'] == region]['sales'],
                    mode='lines',
                    name=region.capitalize(),
                    hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br>' +
                                  '<b>Sales</b>: $%{y:,.2f}<br>' +
                                  '<extra></extra>'
                )
                for region in df['region'].unique()
            ],
            'layout': go.Layout(
                xaxis={
                    'title': 'Date',
                    'showgrid': True,
                    'gridcolor': '#E0E0E0'
                },
                yaxis={
                    'title': 'Daily Sales by Region ($)',
                    'showgrid': True,
                    'gridcolor': '#E0E0E0'
                },
                hovermode='x unified',
                plot_bgcolor='#FAFAFA',
                paper_bgcolor='white',
                margin={'l': 60, 'r': 40, 't': 40, 'b': 60},
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                # Add vertical line to mark the price increase date
                shapes=[
                    dict(
                        type='line',
                        x0='2021-01-15',
                        x1='2021-01-15',
                        y0=0,
                        y1=1,
                        yref='paper',
                        line=dict(
                            color='red',
                            width=2,
                            dash='dash'
                        )
                    )
                ]
            )
        }
    ),
    
    # Statistics summary
    html.Div([
        html.H3('Key Insights', 
                style={'textAlign': 'center', 'color': '#555', 'marginTop': '40px', 'marginBottom': '20px'}),
        html.Div(id='statistics', style={'textAlign': 'center', 'fontSize': '18px'})
    ])
], style={'padding': '20px', 'fontFamily': 'Arial, sans-serif'})

# Calculate statistics for display
price_increase_date = pd.Timestamp('2021-01-15')
before_increase = daily_sales[daily_sales['date'] < price_increase_date]['sales'].mean()
after_increase = daily_sales[daily_sales['date'] >= price_increase_date]['sales'].mean()
percentage_change = ((after_increase - before_increase) / before_increase) * 100

# Add callback to display statistics
@app.callback(
    dash.dependencies.Output('statistics', 'children'),
    dash.dependencies.Input('sales-chart', 'figure')
)
def update_statistics(_):
    return html.Div([
        html.Div([
            html.Strong('Average Daily Sales Before Price Increase: '),
            html.Span(f'${before_increase:,.2f}', style={'color': '#4A90E2'})
        ], style={'marginBottom': '10px'}),
        html.Div([
            html.Strong('Average Daily Sales After Price Increase: '),
            html.Span(f'${after_increase:,.2f}', style={'color': '#E24A4A'})
        ], style={'marginBottom': '10px'}),
        html.Div([
            html.Strong('Change: '),
            html.Span(
                f'{percentage_change:+.2f}%', 
                style={'color': 'green' if percentage_change > 0 else 'red', 'fontSize': '20px', 'fontWeight': 'bold'}
            )
        ], style={'marginTop': '20px'})
    ])

# Run the app
if __name__ == '__main__':
    print("\n" + "="*60)
    print("Soul Foods - Pink Morsel Sales Visualizer")
    print("="*60)
    print(f"\nAverage sales BEFORE Jan 15, 2021: ${before_increase:,.2f}")
    print(f"Average sales AFTER Jan 15, 2021:  ${after_increase:,.2f}")
    print(f"Change: {percentage_change:+.2f}%")
    print("\n" + "="*60)
    print("Starting Dash app on http://127.0.0.1:8050/")
    print("="*60 + "\n")
    app.run(debug=True)
