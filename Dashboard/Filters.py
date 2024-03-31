import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Output, Input
import calendar
import locale
from Parsing_data import df

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

#Ok?
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
                        style={'display': 'block', 
                        #'backgroundColor': '#00FFFF',   #HEX-коды цветов
                        'fontSize': '15px',
                        'margin-left': '10px', 
                        'width': '200px', 
                        'height': '105px'
                        })
#
                            
choosing_a_year = html.Div(children=[
                    html.H3(children='Выберете год'),
                        html.P([
                        dcc.Checklist(            
                            ['2022','2023'],
                            ['2022','2023'], 
                            id='choose_a_year'
                                    ),
                           html.Hr()
                           ])
                        ],
                        style={'display': 'block', 
                        #'backgroundColor': '#00FFFF',   #HEX-коды цветов
                        'fontSize': '15px',
                        'margin-left': '10px', 
                        'width': '200px', 
                        'height': '90px'
                        })

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
                            style={
                                'display': 'block', 
                                #'backgroundColor': '#00FFFF',   #HEX-коды цветов
                                'fontSize': '14px',
                                'margin-left': '35px', 
                                'width': '20px', 
                                'height': '3px'}
                                )
                        ],   
                        style={'display': 'block', 
                        #'backgroundColor': '#00FFFF',   #HEX-коды цветов
                        'fontSize': '15px',
                        'margin-left': '10px', 
                        'width': '200px', 
                        'height': '360px'
                        }
                    )

table=html.Div([
    html.H1('Табличные данные'),
    html.Div(id='datatable-container')
            ])