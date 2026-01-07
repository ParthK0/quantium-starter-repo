import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objs as go

# Read the processed sales data
df = pd.read_csv('data/output.csv')

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Sort by date
df = df.sort_values('date')

# Create the Dash app
app = dash.Dash(__name__)

# Define custom CSS styles
header_style = {
    'background': 'linear-gradient(135deg, #FF1493 0%, #FF69B4 100%)',
    'padding': '40px 20px',
    'borderRadius': '15px',
    'marginBottom': '30px',
    'boxShadow': '0 8px 16px rgba(255, 20, 147, 0.3)',
    'textAlign': 'center'
}

title_style = {
    'color': 'white',
    'marginBottom': '10px',
    'fontFamily': 'Arial, sans-serif',
    'fontWeight': 'bold',
    'textShadow': '2px 2px 4px rgba(0,0,0,0.2)'
}

subtitle_style = {
    'color': 'white',
    'marginBottom': '0',
    'fontFamily': 'Arial, sans-serif',
    'fontSize': '20px',
    'fontWeight': '300'
}

filter_container_style = {
    'background': 'white',
    'padding': '25px',
    'borderRadius': '12px',
    'marginBottom': '25px',
    'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
    'border': '2px solid #FFB6C1'
}

chart_container_style = {
    'background': 'white',
    'padding': '20px',
    'borderRadius': '12px',
    'marginBottom': '25px',
    'boxShadow': '0 4px 12px rgba(0,0,0,0.1)'
}

stats_container_style = {
    'background': 'linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%)',
    'padding': '30px',
    'borderRadius': '12px',
    'boxShadow': '0 4px 12px rgba(0,0,0,0.1)',
    'border': '2px solid #FFB6C1'
}

# Define the layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1('🍬 Soul Foods - Pink Morsel Sales Analysis', style=title_style),
        html.H3('Sales Performance: Before vs After Price Increase (January 15, 2021)', 
                style=subtitle_style)
    ], style=header_style),
    
    # Filter Controls
    html.Div([
        html.Div([
            html.Label('📍 Filter by Region:', 
                      style={'fontSize': '18px', 'fontWeight': 'bold', 'color': '#FF1493', 
                             'marginBottom': '15px', 'display': 'block'}),
            dcc.RadioItems(
                id='region-filter',
                options=[
                    {'label': ' 🌍 All Regions', 'value': 'all'},
                    {'label': ' ⬆️ North', 'value': 'north'},
                    {'label': ' ⬇️ South', 'value': 'south'},
                    {'label': ' ➡️ East', 'value': 'east'},
                    {'label': ' ⬅️ West', 'value': 'west'}
                ],
                value='all',
                inline=True,
                style={'fontSize': '16px'},
                labelStyle={
                    'display': 'inline-block',
                    'marginRight': '25px',
                    'padding': '10px 20px',
                    'background': '#FFF0F5',
                    'borderRadius': '25px',
                    'cursor': 'pointer',
                    'transition': 'all 0.3s',
                    'border': '2px solid #FFB6C1'
                }
            )
        ])
    ], style=filter_container_style),
    
    # Line chart
    html.Div([
        dcc.Graph(id='sales-chart')
    ], style=chart_container_style),
    
    # Regional breakdown
    html.Div([
        html.Div([
            html.H3('📊 Sales by Region', 
                    style={'textAlign': 'center', 'color': '#FF1493', 'marginBottom': '20px'})
        ]),
        dcc.Graph(id='regional-sales-chart')
    ], style=chart_container_style),
    
    # Statistics summary
    html.Div([
        html.H3('💡 Key Insights', 
                style={'textAlign': 'center', 'color': '#FF1493', 'marginBottom': '25px', 
                       'fontSize': '28px', 'fontWeight': 'bold'}),
        html.Div(id='statistics')
    ], style=stats_container_style)
], style={
    'padding': '30px',
    'fontFamily': 'Arial, sans-serif',
    'background': 'linear-gradient(to bottom, #FFF5F7 0%, #FFFFFF 100%)',
    'minHeight': '100vh'
})

# Calculate statistics for display
price_increase_date = pd.Timestamp('2021-01-15')

# Callback to update main sales chart based on region filter
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_sales_chart(selected_region):
    if selected_region == 'all':
        filtered_df = df.groupby('date')['sales'].sum().reset_index()
        title_text = 'Total Daily Sales - All Regions'
        line_color = '#FF1493'
    else:
        filtered_df = df[df['region'] == selected_region].copy()
        title_text = f'Daily Sales - {selected_region.capitalize()} Region'
        region_colors = {'north': '#4169E1', 'south': '#FF6347', 'east': '#32CD32', 'west': '#FFD700'}
        line_color = region_colors.get(selected_region, '#FF1493')
    
    figure = {
        'data': [
            go.Scatter(
                x=filtered_df['date'],
                y=filtered_df['sales'],
                mode='lines+markers',
                name='Daily Sales',
                line=dict(color=line_color, width=3),
                marker=dict(size=6, color=line_color, symbol='circle'),
                fill='tozeroy',
                fillcolor=f'rgba({int(line_color[1:3], 16)}, {int(line_color[3:5], 16)}, {int(line_color[5:7], 16)}, 0.1)',
                hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br>' +
                              '<b>Sales</b>: $%{y:,.2f}<br>' +
                              '<extra></extra>'
            )
        ],
        'layout': go.Layout(
            title={
                'text': title_text,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 20, 'color': '#FF1493', 'family': 'Arial'}
            },
            xaxis={
                'title': 'Date',
                'showgrid': True,
                'gridcolor': '#E8E8E8',
                'titlefont': {'size': 14, 'color': '#555'}
            },
            yaxis={
                'title': 'Daily Sales ($)',
                'showgrid': True,
                'gridcolor': '#E8E8E8',
                'titlefont': {'size': 14, 'color': '#555'}
            },
            hovermode='x unified',
            plot_bgcolor='#FAFAFA',
            paper_bgcolor='white',
            margin={'l': 70, 'r': 40, 't': 60, 'b': 60},
            shapes=[
                dict(
                    type='line',
                    x0='2021-01-15',
                    x1='2021-01-15',
                    y0=0,
                    y1=1,
                    yref='paper',
                    line=dict(color='#DC143C', width=3, dash='dash')
                )
            ],
            annotations=[
                dict(
                    x='2021-01-15',
                    y=1,
                    yref='paper',
                    text='💰 Price Increase<br>Jan 15, 2021',
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor='#DC143C',
                    ax=0,
                    ay=-50,
                    font=dict(color='#DC143C', size=13, family='Arial'),
                    bgcolor='rgba(255, 255, 255, 0.95)',
                    bordercolor='#DC143C',
                    borderwidth=2,
                    borderpad=8
                )
            ]
        )
    }
    return figure

# Callback to update regional breakdown chart
@app.callback(
    Output('regional-sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_regional_chart(selected_region):
    region_colors = {
        'north': '#4169E1',
        'south': '#FF6347',
        'east': '#32CD32',
        'west': '#FFD700'
    }
    
    if selected_region == 'all':
        # Show all regions
        traces = [
            go.Scatter(
                x=df[df['region'] == region]['date'],
                y=df[df['region'] == region]['sales'],
                mode='lines',
                name=region.capitalize(),
                line=dict(color=region_colors[region], width=2),
                hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br>' +
                              '<b>Sales</b>: $%{y:,.2f}<br>' +
                              '<extra></extra>'
            )
            for region in df['region'].unique()
        ]
    else:
        # Show only selected region
        traces = [
            go.Scatter(
                x=df[df['region'] == selected_region]['date'],
                y=df[df['region'] == selected_region]['sales'],
                mode='lines+markers',
                name=selected_region.capitalize(),
                line=dict(color=region_colors[selected_region], width=3),
                marker=dict(size=5),
                hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br>' +
                              '<b>Sales</b>: $%{y:,.2f}<br>' +
                              '<extra></extra>'
            )
        ]
    
    figure = {
        'data': traces,
        'layout': go.Layout(
            xaxis={
                'title': 'Date',
                'showgrid': True,
                'gridcolor': '#E8E8E8'
            },
            yaxis={
                'title': 'Daily Sales ($)',
                'showgrid': True,
                'gridcolor': '#E8E8E8'
            },
            hovermode='x unified',
            plot_bgcolor='#FAFAFA',
            paper_bgcolor='white',
            margin={'l': 70, 'r': 40, 't': 40, 'b': 60},
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.9)',
                bordercolor='#FFB6C1',
                borderwidth=2
            ),
            shapes=[
                dict(
                    type='line',
                    x0='2021-01-15',
                    x1='2021-01-15',
                    y0=0,
                    y1=1,
                    yref='paper',
                    line=dict(color='#DC143C', width=2, dash='dash')
                )
            ]
        )
    }
    return figure

# Callback to update statistics based on region filter
@app.callback(
    Output('statistics', 'children'),
    Input('region-filter', 'value')
)
def update_statistics(selected_region):
    if selected_region == 'all':
        filtered_df = df.groupby('date')['sales'].sum().reset_index()
    else:
        filtered_df = df[df['region'] == selected_region].copy()
    
    before_increase = filtered_df[filtered_df['date'] < price_increase_date]['sales'].mean()
    after_increase = filtered_df[filtered_df['date'] >= price_increase_date]['sales'].mean()
    percentage_change = ((after_increase - before_increase) / before_increase) * 100
    
    return html.Div([
        html.Div([
            html.Div([
                html.Div('📉 Before Price Increase', 
                        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '5px'}),
                html.Div(f'${before_increase:,.2f}', 
                        style={'fontSize': '32px', 'fontWeight': 'bold', 'color': '#4A90E2'})
            ], style={'flex': '1', 'textAlign': 'center', 'padding': '20px', 
                     'background': 'white', 'borderRadius': '10px', 'margin': '10px',
                     'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'}),
            
            html.Div([
                html.Div('📈 After Price Increase', 
                        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '5px'}),
                html.Div(f'${after_increase:,.2f}', 
                        style={'fontSize': '32px', 'fontWeight': 'bold', 'color': '#E24A4A'})
            ], style={'flex': '1', 'textAlign': 'center', 'padding': '20px',
                     'background': 'white', 'borderRadius': '10px', 'margin': '10px',
                     'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'}),
            
            html.Div([
                html.Div('📊 Change', 
                        style={'fontSize': '16px', 'color': '#666', 'marginBottom': '5px'}),
                html.Div(f'{percentage_change:+.2f}%', 
                        style={'fontSize': '32px', 'fontWeight': 'bold', 
                               'color': '#22C55E' if percentage_change > 0 else '#EF4444'})
            ], style={'flex': '1', 'textAlign': 'center', 'padding': '20px',
                     'background': 'white', 'borderRadius': '10px', 'margin': '10px',
                     'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'})
        ], style={'display': 'flex', 'justifyContent': 'space-around', 'flexWrap': 'wrap'}),
        
        html.Div(
            f'{"🎉 Sales increased significantly!" if percentage_change > 0 else "⚠️ Sales decreased"}',
            style={
                'textAlign': 'center',
                'marginTop': '25px',
                'fontSize': '20px',
                'fontWeight': 'bold',
                'color': '#FF1493',
                'padding': '15px',
                'background': 'white',
                'borderRadius': '10px',
                'boxShadow': '0 2px 8px rgba(0,0,0,0.1)'
            }
        )
    ])

# Run the app
if __name__ == '__main__':
    # Calculate overall statistics for initial display
    daily_sales = df.groupby('date')['sales'].sum().reset_index()
    before_increase = daily_sales[daily_sales['date'] < price_increase_date]['sales'].mean()
    after_increase = daily_sales[daily_sales['date'] >= price_increase_date]['sales'].mean()
    percentage_change = ((after_increase - before_increase) / before_increase) * 100
    
    print("\n" + "="*60)
    print("🍬 Soul Foods - Pink Morsel Sales Visualizer 🍬")
    print("="*60)
    print(f"\nAverage sales BEFORE Jan 15, 2021: ${before_increase:,.2f}")
    print(f"Average sales AFTER Jan 15, 2021:  ${after_increase:,.2f}")
    print(f"Change: {percentage_change:+.2f}%")
    print("\n" + "="*60)
    print("Starting Dash app on http://127.0.0.1:8050/")
    print("="*60 + "\n")
    app.run(debug=True)
