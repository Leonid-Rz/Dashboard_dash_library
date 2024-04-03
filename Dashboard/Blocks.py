import pandas as pd
from dash import Dash, dcc, html, dash_table, callback, Output, Input
import dash_bootstrap_components as dbc
import calendar
import locale

from Parsing_data import df

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

head = html.Div(children=[
    'Мониторинг ОКС Новгородская область'
], className='heading'
)


card_total_ASC=dbc.Card(children=[
                        dbc.CardHeader("Всего ОКС", className='card_header'),
                        dbc.CardBody(html.P(id='total_ASC', className='card_text'))
                        ], className='_card_'
                    )

card_ACS_with_ST= dbc.Card(children=[
                        dbc.CardHeader("ОКС с подъемом ST", className='card_header'),
                        dbc.CardBody(html.P(id='ACS_with_ST', className='card_text'))
                        ], className='_card_'
                    )

card_ACS_without_ST=dbc.Card(children=[
                       dbc.CardHeader("ОКС без подъема ST", className='card_header'),
                        dbc.CardBody(html.P(id='ACS_without_ST', className='card_text'))
                        ], className='_card_'
                    )

card_PCI_coverage =dbc.Card(children=[
                        dbc.CardHeader("Охват ЧКВ", className='card_header'),
                        dbc.CardBody(html.P(id='PCI_coverage', className='card_text'))
                        ], className='_card_'
                    )
card_ACS_mort_rate=dbc.Card(children=[
                        dbc.CardHeader("Летальность при ОКС", className='card_header'),
                        dbc.CardBody(html.P(id='ACS_mort_rate', className='card_text'))
                        ], className='_card_'
                    )
card_MI_mortality_rate=dbc.Card(children=[
                        dbc.CardHeader("Летальность при ИМ", className='card_header'),
                        dbc.CardBody(html.P(id='MI_mortality_rate', className='card_text'))
                        ], className='_card_'
                    )

line_of_cards= html.Div(children=[
        card_total_ASC,
        card_ACS_with_ST,
        card_ACS_without_ST,
        card_PCI_coverage,
        card_ACS_mort_rate,
        card_MI_mortality_rate
], className='cards_stack'
)

choosing_a_hospital = html.Div(children=[
                        html.H3(children='Выберете больницу', style={'fontWeight': 550}),
                        html.P([
                            dcc.Checklist(            
                                ['ГОБУЗ "Боровичская ЦРБ"','ГОБУЗ "Старорусская ЦРБ"', 'ГОБУЗ "НОКБ"'],
                                ['ГОБУЗ "Боровичская ЦРБ"','ГОБУЗ "Старорусская ЦРБ"', 'ГОБУЗ "НОКБ"'], 
                                id='choose_a_hospital'
                                ),
                        html.Hr()
                                ], className='sidebar_text_style')
                            ]
                        )
                      
choosing_a_year = html.Div(children=[
                    html.H3(children='Выберете год', style={'fontWeight': 550}),
                        html.P([
                        dcc.RadioItems(            
                            ['2022','2023', '2024'],
                            '2022', 
                            id='choose_a_year'
                                    ),
                           html.Hr()
                           ], className='sidebar_text_style')
                        ]
                        )

choosing_the_month= html.Div(children=[
                        html.H3(children='Выберете месяц', style={'fontWeight': 550}),
                        html.Div(children=[
                            dcc.RangeSlider(
                                min=1, max=12, 
                                step=1,
                                value=[1,12],
                                marks={i:{'label': calendar.month_name[i], 'style': {'fontSize': '17px', 'color':'black'}} for i in range(1, 13)},
                                tooltip={"placement": "bottom", "always_visible": False},
                                vertical = True,
                                verticalHeight = 400,
                                id='monthly_slider'
                                )], className='month_slider_style'
                                )
                        ]
                        )

#block_table=html.Div(children=[
 #   html.Div('Табличные данные', className='heading_table'),
  #  html.Div(id='datatable-container',className='b_table')])

block_sidebar= html.Div( children= [
                    choosing_a_hospital,
                    choosing_a_year, 
                    choosing_the_month
                    ], className='sidebar'
                    )
