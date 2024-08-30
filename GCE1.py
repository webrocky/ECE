import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load datasets
elderly_specific_data = pd.read_csv('C:/Users/Asus/Desktop/GERIATRIC CARE/Dashboard/GCE1/elderly_specific_data.csv')
top_10_countries_data = pd.read_csv('C:/Users/Asus/Desktop/GERIATRIC CARE/Dashboard/GCE1/top_10_countries_elderly.csv')

# Improved country flag function
def get_flag(country_name):
    flags = {
        'United States': '🇺🇸',
        'India': '🇮🇳',
        'Germany': '🇩🇪',
        # Add more countries here
    }
    return flags.get(country_name, '')

# Apply flags to country names
top_10_countries_data['Country'] = top_10_countries_data['Country'].apply(lambda x: get_flag(x) + " " + x)

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1("ECE", style={'textAlign': 'center', 'fontSize': '48px', 'color': '#007BFF', 'fontWeight': 'bold'}),
    html.H2("Top 10 Countries to consider for expanding elderly care services",
            style={'textAlign': 'center', 'fontSize': '24px', 'fontWeight': 'bold'}),
    
    # Horizontal bar chart for top 10 countries
    dcc.Graph(id='top-10-bar'),
    
    # Year slider
    dcc.Slider(
        id='year-slider',
        min=2000,
        max=2030,
        value=2000,
        marks={str(year): str(year) for year in range(2000, 2031)},
        step=1
    ),
    
    # Search section
    html.Div([
        html.H3("Search for a Country", style={'textAlign': 'center', 'marginTop': '20px'}),
        dcc.Dropdown(
            id='country-selector',
            options=[{'label': country, 'value': country} for country in elderly_specific_data['country'].unique()],
            placeholder='Select a country...',
            style={'width': '50%', 'margin': 'auto'}
        ),
    ]),
    
    # Container for country-specific plots
    html.Div(id='country-plots', style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px', 'marginTop': '20px'}),
    
    # Comparison Section
    html.H2("Comparison Section", style={'textAlign': 'center', 'fontSize': '24px', 'fontWeight': 'bold', 'marginTop': '50px'}),
    
    # Dropdowns for comparison section
    html.Div([
        dcc.Dropdown(
            id='compare-dropdown-1',
            options=[{'label': country, 'value': country} for country in elderly_specific_data['country'].unique()],
            placeholder='Select the first country...',
            style={'width': '45%', 'display': 'inline-block', 'marginRight': '5%'}
        ),
        dcc.Dropdown(
            id='compare-dropdown-2',
            options=[{'label': country, 'value': country} for country in elderly_specific_data['country'].unique()],
            placeholder='Select the second country...',
            style={'width': '45%', 'display': 'inline-block'}
        ),
    ], style={'textAlign': 'center', 'marginTop': '20px'}),
    
    html.Div(id='comparison-plots', style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px', 'marginTop': '20px'})
])

# Callback for updating the top 10 bar chart (horizontal)
@app.callback(
    Output('top-10-bar', 'figure'),
    Input('year-slider', 'value'))
def update_top_10_chart(selected_year):
    filtered_data = top_10_countries_data[top_10_countries_data['Year'] == selected_year]
    
    fig = px.bar(
        filtered_data,
        y='Country',
        x='Predicted Composite Score',
        orientation='h',
        color='Country',
        title=f"Elderly Care Expansion Score by Country in {selected_year}",
        labels={"Predicted Composite Score": "Elderly Care Expansion Score"},
        template="plotly_dark"  # Modern dark theme
    )
    
    fig.update_layout(showlegend=True, yaxis_title="Country", xaxis_title="Elderly Care Expansion Score")
    
    return fig

# Callback for generating multiple plots for the selected country with different chart types
@app.callback(
    Output('country-plots', 'children'),
    Input('country-selector', 'value'))
def generate_country_plots(country_name):
    if not country_name:
        return []
    data = elderly_specific_data[elderly_specific_data['country'] == country_name]
    
    plots = []
    # Line chart for population_60_plus
    fig1 = px.line(data, x='Year', y='population_60_plus', title="Elderly Population (60+) Over Time", template="plotly_dark")
    plots.append(dcc.Graph(figure=fig1))
    
    # Area chart for GDP contribution
    fig2 = px.area(data, x='Year', y='gdp_elderly', title="GDP Contribution by Elderly Population", template="plotly_dark")
    plots.append(dcc.Graph(figure=fig2))
    
    # Bar chart for healthcare expenditure
    fig3 = px.bar(data, x='Year', y='che_elderly', title="Total Healthcare Expenditure Over Time", template="plotly_dark")
    plots.append(dcc.Graph(figure=fig3))
    
    # Scatter plot for government vs private expenditure
    fig4 = px.scatter(data, x='gghed_elderly', y='pvtd_elderly',
                      title="Government vs Private Healthcare Expenditure",
                      labels={"gghed_elderly": "Government Expenditure", "pvtd_elderly": "Private Expenditure"},
                      template="plotly_dark")
    plots.append(dcc.Graph(figure=fig4))
    
    return plots

# Callback for generating comparison plots
@app.callback(
    Output('comparison-plots', 'children'),
    [Input('compare-dropdown-1', 'value'), Input('compare-dropdown-2', 'value')])
def generate_comparison_plots(country1, country2):
    if not country1 or not country2:
        return []
    
    data1 = elderly_specific_data[elderly_specific_data['country'] == country1]
    data2 = elderly_specific_data[elderly_specific_data['country'] == country2]
    
    plots = []
    # Line chart comparison for population_60_plus
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=data1['Year'], y=data1['population_60_plus'], mode='lines', name=country1))
    fig1.add_trace(go.Scatter(x=data2['Year'], y=data2['population_60_plus'], mode='lines', name=country2))
    fig1.update_layout(title="Comparison of Elderly Population (60+) Over Time", template="plotly_dark")
    plots.append(dcc.Graph(figure=fig1))
    
    # Area chart comparison for GDP contribution
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=data1['Year'], y=data1['gdp_elderly'], fill='tozeroy', mode='none', name=country1))
    fig2.add_trace(go.Scatter(x=data2['Year'], y=data2['gdp_elderly'], fill='tozeroy', mode='none', name=country2))
    fig2.update_layout(title="Comparison of GDP Contribution by Elderly Population", template="plotly_dark")
    plots.append(dcc.Graph(figure=fig2))
    
    # Bar chart comparison for healthcare expenditure
    fig3 = go.Figure()
    fig3.add_trace(go.Bar(x=data1['Year'], y=data1['che_elderly'], name=country1))
    fig3.add_trace(go.Bar(x=data2['Year'], y=data2['che_elderly'], name=country2))
    fig3.update_layout(barmode='group', title="Comparison of Healthcare Expenditure", template="plotly_dark")
    plots.append(dcc.Graph(figure=fig3))
    
    return plots

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
