from dash import Dash, html, dcc, dash_table, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_html_components as html

from Parsing_data import df 
from Blocks import *
from Calculation import calculations

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(children= [
                head,
                html.Div(children= [
                    block_sidebar,
                    line_of_cards
                    ],className='flex'
                    ),
                html.Div( children= [
                    table
                     ]
                     )
                    ],className='big_color'
                )

@callback(
    Output('total_ASC', 'children'),
    Output('ACS_with_ST', 'children'),
    Output('ACS_without_ST', 'children'),
    Output('datatable-container', 'children'),
    Input('choose_a_hospital', 'value'),
    Input('monthly_slider', 'value'),
    Input('choose_a_year', 'value')
)
def intermediate_function (*args, **kwargs):
    return calculations (*args, **kwargs)

if __name__ == '__main__':
    app.run(debug=True)

