#import pandas as pd
#from dash import Dash, dcc, html, dash_table, callback, Output, Input
#import dash_bootstrap_components as dbc
#import plotly.express as px
#from plotly.subplots import make_subplots
#import plotly.graph_objects as go


#HEX-коды цветов

hospital_stile = {'display': 'block', 
                    'fontSize': '15px',
                    'margin-left': '10px', 
                    'width': '220px', 
                    'height': '105px'
                }

Body_stile={'display': 'block', 
            'backgroundColor': '#87CEFA',   #HEX-коды цветов
            'fontSize': '15px',
            'margin-left': '0px', 
            'margin-right': '0px',
            'width': '250px', 
            'height': '1000px'
                 }

year_style={'display': 'block',
            'fontSize': '15px',
            'margin-left': '10px', 
            'width': '220px', 
            'height': '90px'
            }

month_slider_style={'display': 'block', 
                    'fontSize': '14px',
                    'margin-left': '35px', 
                    'width': '20px', 
                    }

month_style = {'display': 'block', 
                'fontSize': '15px',
                'margin-left': '10px', 
                'width': '200px', 
                'height': '400px'
                }

table_style={'display': 'block', 
            'backgroundColor': '#FFFFFF',
            'fontSize': '15px',
            'margin-left': '0px', 
            'margin-right': '0px',
            'width': '1700px', 
            'height': '360px'
                 }

b_table = {'whiteSpace': 'normal',
        'backgroundColor': 'white', 
        'height': 'auto'}



