from dash import Dash, html, dcc, dash_table, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_html_components as html

from Parsing_data import df 
from Blocks import choosing_a_hospital, choosing_a_year, choosing_the_month, table, line_of_cards
from Calculation import calculations
from Style import Body_stile

app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(children= [
            html.Div(children = line_of_cards), 
            html.Div( children= [
                    choosing_a_hospital,
                    choosing_a_year, 
                    choosing_the_month, 
                    table,
                    ],
                    style=Body_stile
                    )
                ])

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

