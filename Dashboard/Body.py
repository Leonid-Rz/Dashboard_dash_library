from dash import Dash, html, dcc, dash_table, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import dash_html_components as html

from Parsing_data import df 
from Blocks import choosing_a_hospital, choosing_a_year, choosing_the_month, table
from Calculation import calculations
from Style import Body_stile

app = Dash(__name__)

card_total_ASC= dbc.Card(children=[
                        dbc.CardHeader("Всего ОКС"),
                        dbc.CardBody(html.P(id='total_ASC'))
                        ])

card_ACS_with_ST= dbc.Card(children=[
                        dbc.CardHeader("ОКС с подъемом ST"),
                        dbc.CardBody(html.P(id='ACS_with_ST'))
                        ])

card_ACS_without_ST= dbc.Card(children=[
                        dbc.CardHeader("ОКС без подъема ST"),
                        dbc.CardBody(html.P(id='ACS_without_ST'))
                        ])

app.layout =html.Div(children= [ 
                html.Div(children= [ 
                    dbc.Container(children= [
                                            card_total_ASC
                                            ],
                                        style={
                                            'border': '2px solid black',
                                            'padding': '20px',
                                            'display': 'block', 
                                            'backgroundColor': '#DC143C',   #HEX-коды цветов
                                            'margin-left': '0px', 
                                            'margin-right': '0px',
                                            'width': '150px', 
                                            'height': '75px'}),
                    dbc.Container(children= [
                                            card_ACS_with_ST
                                            ],
                                        style={
                                            'border': '2px solid black',
                                            'padding': '20px',
                                            'display': 'block', 
                                            'backgroundColor': '#DC143C',   #HEX-коды цветов
                                            'margin-left': '0px', 
                                            'margin-right': '0px',
                                            'width': '150px', 
                                            'height': '75px'}),
                    dbc.Container(children= [
                                            card_ACS_without_ST
                                            ],
                                        style={
                                            'border': '2px solid black',
                                            'padding': '20px',
                                            'display': 'block', 
                                            'backgroundColor': '#DC143C',   #HEX-коды цветов
                                            'margin-left': '0px', 
                                            'margin-right': '0px',
                                            'width': '150px', 
                                            'height': '75px'})
                                    ]),
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

