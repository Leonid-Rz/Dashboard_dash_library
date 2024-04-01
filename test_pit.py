import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Output, Input
import calendar
import locale

from Parsing_data import df
from Style import hospital_stile, year_style, month_slider_style, month_style, table_style

import pandas as pd
from dash import Dash, html, dcc, dash_table, callback, Output, Input

#import plotly.express as px
#from plotly.subplots import make_subplots
#import plotly.graph_objects as go

from Parsing_data import df
from Style import b_table


locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

choosing_a_hospital = html.Div(children=[
                        html.H3(children='Выберете больницу'),
                        html.P([
                            dcc.Checklist(            
                                ['ГОБУЗ "Боровичская ЦРБ"','ГОБУЗ "Старорусская ЦРБ"', 'ГОБУЗ "НОКБ"'],
                                ['ГОБУЗ "Боровичская ЦРБ"','ГОБУЗ "Старорусская ЦРБ"', 'ГОБУЗ "НОКБ"'], 
                                id='choose_a_hospital'
                                ),
                        html.Hr()
                                ])
                            ],
                        style=hospital_stile
                        )
                      
choosing_a_year = html.Div(children=[
                    html.H3(children='Выберете год'),
                        html.P([
                        dcc.RadioItems(            
                            ['2022','2023', '2024'],
                            '2022', 
                            id='choose_a_year'
                                    ),
                           html.Hr()
                           ])
                        ],
                        style=year_style
                        )

choosing_the_month= html.Div(children=[
                        html.H3(children='Выберете месяц'),
                        html.Div(children=[
                            dcc.RangeSlider(
                                min=1, max=12, 
                                step=1,
                                value=[1,12],
                                marks={i: calendar.month_name[i] for i in range(1, 13)},
                                tooltip={"placement": "bottom", "always_visible": False},
                                vertical = True,
                                verticalHeight = 300,
                                id='monthly_slider'
                                )], 
                            style= month_slider_style
                                )
                        ],   
                        style=month_style 
                        )

table=html.Div(children=[
    html.H1('Табличные данные'),
    html.Div(id='datatable-container')],style=table_style)

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



def calculations (selected_hospital, month, year ):
        #Фильтр
            #Основная таблица
            #t_year=[int (x) for x in year]
            new_df = df[(df['Hospital'].isin(selected_hospital)) & (df['Month'].isin(range(month[0], month [1]+1))) & (df['Date'].dt.to_period('Y') == year)]
            table= dash_table.DataTable(style_data=b_table,
                            data=new_df.to_dict('records'), 
                            page_size=15
                            )
            # Всего ОКС
            total_ACS = df.loc[(df['№ п/п'] == 47) &
                            (df['Date'].dt.to_period('Y') == year) &
                            (df['Date'].dt.month.isin(range(month[0], month [1]+1))) &
                            (df['Hospital'].isin(selected_hospital)),'Value'].sum()
            #Кол-во ОКС с подъемом ST
            ACS_with_ST = df.loc[(df['№ п/п'] == '47.1') &
                            (df['Date'].dt.to_period('Y') == year) &
                            (df['Date'].dt.month.isin(range(month[0], month [1]+1))) &
                            (df['Hospital'].isin(selected_hospital))].shape[0]
            #Кол-во ОКС без подъема ST
            ACS_without_ST = df.loc[(df['№ п/п'] == '47.2') &
                            (df['Date'].dt.to_period('Y') == year) &
                            (df['Date'].dt.month.isin(range(month[0], month [1]+1))) &
                            (df['Hospital'].isin(selected_hospital))].shape[0]

            return total_ACS, ACS_with_ST, ACS_without_ST, table

