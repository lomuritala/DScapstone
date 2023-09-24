# Import required libraries
#
import dash
import pandas as pd
from dash import Dash, html, dash_table, dcc, Output, Input
import plotly.express as px
#
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
df = spacex_df
df.rename(columns = {'Launch Site': 'LaunchSite', 'class': 'Class', 'Payload Mass (kg)': 'PayloadMass' }, inplace=True)

# Create piechart data
pie_data = df.where(df.Class==1).dropna()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.P('Successful Launches Per Site'),
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}
                                    ],
                                    value='Select a Launch Site',
                                    placeholder="Select a Launch Site: ",
                                    searchable=True
                                    ),
                                    html.Div(id='launch-site'),
                                 html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart',
                                    figure=px.pie(pie_data, values = 'Class', names = 'LaunchSite', title='Total Successful Launches by Site'),
                                    ),
                                ),
                                html.Div(id='pie-site'),
                                #html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                html.Div([
                                    dcc.RangeSlider(
                                        id='payload-slider', 
                                        min=0, 
                                        max=10000, 
                                        step=1000,
                                        value=[df['PayloadMass'].min(), df['PayloadMass'].max()]
                                        )
                                    ]
                                ),
                                #html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                #plot_data = spacex_df
                                html.P('Correlation between payload and launch success'),
                                html.Div(dcc.Graph(id='success-payload-scatter-chart',
                                    figure = px.scatter(df, x = "PayloadMass", y = "Class", color = 'Booster Version Category', hover_name = 'LaunchSite'),
                                    )
                                )
                            ]
                        )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
        [Output(component_id='success-pie-chart', component_property='figure')],
        [Input(component_id='site-dropdown', component_property="value")]
    )

def print_pie(r_val):
    filtered_df = df
    if r_val == 'ALL' :
        filtered_df = df.where(df.Class == 1)
        fig = px.pie(filtered_df, values='Class', names='LaunchSite', title='Total Successful Launches by Site')
        return [fig]
    else : 
        filtered_df = df.where(df.LaunchSite == r_val).dropna()
        pie_data = filtered_df.groupby(['LaunchSite', 'Class']).size().reset_index(name='Counts')
        fig = px.pie(pie_data, values='Counts', names='Class', title='Total Successful Launches from Site: '+r_val)
        return [fig]

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
        [Output(component_id='success-payload-scatter-chart',component_property="figure")],
        [Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
        ]
    )

def update_scatter(site_val, p_val):
    filtered_df = df
    if site_val == 'ALL' :
        filtered_df = df
        filtered_df = filtered_df.where(filtered_df.PayloadMass <= p_val[-1]).dropna()
        filtered_df = filtered_df.where(filtered_df.PayloadMass >= p_val[0]).dropna()
        fig = px.scatter(filtered_df, x = "PayloadMass", y = "Class", color = 'Booster Version Category', title=site_val )
        return [fig]
    else : 
        filtered_df = df.where(df.LaunchSite == site_val).dropna()
        filtered_df = filtered_df.where(filtered_df.PayloadMass <= p_val[-1]).dropna()
        filtered_df = filtered_df.where(filtered_df.PayloadMass >= p_val[0]).dropna()
        fig = px.scatter(filtered_df, x = "PayloadMass", y = "Class", color = 'Booster Version Category', title=site_val )
        return [fig]


# Run the app
if __name__ == '__main__':
    app.run_server()
