import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Output, Input
import calendar
import locale

from Parsing_data import df
from Style import hospital_stile, year_style, month_slider_style, month_style, table_style

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
                        dcc.Checklist(            
                            ['2022','2023'],
                            ['2022','2023'], 
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