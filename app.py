# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

#### READING DATAFRAME ####

df = pd.read_csv('2019.csv')
df = df.sort_values(by=['Regional Indicator'])
# print(df.head())

options_info = [{'label': str(i), 'value': str(i)} for i in df['Regional Indicator'].unique()]
# print(options_info)

#### DASH SETUP STUFF ####

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div("World Happiness (Gallup Poll 2019)", 
                        style={
                            'height': '100%', 
                            'width':'100%', 
                            'font-size': '3rem',
                            'color': 'rgba(0, 0, 0, 0.75)',
                            'font-family': 'Segoe UI',
                            'font-weight': 'bold',
                            'display': 'flex',
                            'flex-direction': 'column',
                            'justify-content': 'center',
                            'background-color': '#E0E0E0',
                            'box-shadow': '3px 3px 2px rgba(0, 0, 0, 0.2)',
                            'border-radius': '5px',
                            # 'font-size' : 'calc(48px + (72 - 48) * ((100vw - 300px) / (1600 - 300)));'
                        }
                    ), 
                    lg=12,
                    style={
                        'text-align': 'center',
                        'background-color': '#CCCCCC',
                        'padding': '30px 50px 15px 50px',
                    }
                ), 
            ],
            # justify="center",
            style={
                'height': '15vh',
                'margin': 'auto',
                'max-width': '1800px',
                
            },
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.Div(
                                "Region",
                                style={
                                    'font-size': '24px',
                                    'font-weight': 'bold',
                                    'height': '60px',
                                    'padding-top': '25px',
                                    'font-family': 'Segoe UI',
                                },
                            ),
                            dcc.RadioItems(
                                options=options_info,
                                id='region_radios',
                                value='Central and Eastern Europe',
                                style={
                                    'display': 'flex',
                                    'flex-direction': 'column',
                                    'text-align': 'left',
                                    'padding': '20px',
                                    'height': 'calc(100% - 60px)',
                                    'overflow-y': 'auto',
                                    'font-family': 'Segoe UI',
                                },
                            ),
                        ],
                        style={
                            'height': '100%',
                            'width': '100%',
                            'background-color': '#E0E0E0',
                            'box-shadow': '3px 3px 2px rgba(0, 0, 0, 0.2)',
                            'border-radius': '5px',
                        }
                    ),

                    style={
                        'text-align': 'center',  
                        'background-color': '#CCCCCC',
                        'padding': '15px 15px 30px 50px',
                        'height': 'inherit',
                        'display': 'flex',
                        'flex-direction': 'column',

                    },
                    lg=2,
                ),

                dbc.Col(
                    html.Div(
                        dcc.Graph(
                            id='radar_chart',
                            style={
                                'width': '100%',
                                'height': '100%',

                            }
                        ),
                        style={
                            'height': '100%',
                            'width': '100%',
                            'background-color': '#E0E0E0',
                            'box-shadow': '3px 3px 2px rgba(0, 0, 0, 0.2)',
                            'border-radius': '5px',
                            'padding': '5px',
                        }
                    ),
                    style={
                        'text-align': 'center',  
                        'background-color': '#CCCCCC',  
                        'padding': '15px 15px 30px 15px',
                        'height': 'inherit',
                    },
                    lg=6,
                ),

                dbc.Col(
                    html.Div(
                        [
                            dcc.Graph(
                                id="bar_chart",
                                style={
                                    'height': '100%',
                                    'width': '100%',
                                },
                            ),

                        ],
                        style={
                            'height': '100%',
                            'width': '100%',
                            'background-color': '#E0E0E0',
                            'box-shadow': '3px 3px 2px rgba(0, 0, 0, 0.2)',
                            'border-radius': '5px',
                            'padding': '5px',
                        }
                    ),
                    style={
                        'text-align': 'center',  
                        'background-color': '#CCCCCC',  
                        'padding': '15px 50px 30px 15px',
                        'height': 'inherit',
                    },
                    lg=4,
                ),
            ],
            style={
                'height':'85vh',
                'margin': 'auto',
                'max-width': '1800px',
            }
        ),
    ]
, style={
    'width': '100%',
    'justify-content': 'center',
    'background-color': '#CCCCCC', 
})

#### CALLBACK ####

@app.callback(
    [Output('radar_chart', 'figure'),
    Output('bar_chart', 'figure')],
    [Input('region_radios', 'value')])

def update_figure(selected_region):
    ### FILTERING DF ###
    filtered_df = df[df['Regional Indicator'] == (selected_region)]

    filtered_df = filtered_df.sort_values(by=['Score'])

    r_values = [filtered_df['GDP per capita'].mean(), filtered_df['Social support'].mean(), filtered_df['Healthy life expectancy'].mean(), filtered_df['Freedom to make life choices'].mean(), filtered_df['Generosity'].mean()]

    ## FIG 1
    fig1 = go.Figure(data=go.Scatterpolar(
        r=r_values,
        theta=['Avg GDP','Avg Social support','Avg Health', 'Avg Freedom',
            'Avg Generosity'],
        opacity=0.8,
        fill='toself'
    ))

    fig1.update_layout(
        template="seaborn",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        title_text="<b>Average Happiness Statistics</b>",
        title_font = dict(
            size=24,
            family="Segoe UI",
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0,1.6],
            ),
            angularaxis=dict(
                tickfont=dict(
                    family="Segoe UI",
                    size=16,
                ),
            ),
        ),
        showlegend=False,
    )

    ### FIG 2
    fig2 = go.Figure(data=go.Bar(
                x=filtered_df['Score'],
                y=filtered_df['Country or region'],
                opacity=0.8,
                orientation='h'))

    fig2.update_layout(
        template="seaborn",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_tickfont_size=16,
        yaxis_tickfont_size=16,
        yaxis_tickfont_family="Segoe UI",
        title_text="<b>Country Happiness Score</b>",
        title_font = dict(
            size=24,
            family="Segoe UI",
        ),

    )

    return fig1, fig2

#### NAME MAIN ####

if __name__ == '__main__':
    app.run_server(debug=True)