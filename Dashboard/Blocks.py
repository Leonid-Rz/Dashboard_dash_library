from dash import dcc, html
import dash_bootstrap_components as dbc

month_names = [
    '_', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
]

#Заголовок страницы
head = html.Div(children=[
                     'Мониторинг ОКС города Спрингфилда'
                        ], className='heading'
                )

#Карточка всего ОКС
card_total_ASC=dbc.Card(children=[
                        dbc.CardHeader("Всего ОКС", className='card_header'),
                        dbc.CardBody(html.P(id='total_ASC', className='card_text'))
                        ], className='_card_'
                    )

#Карточка ОКС с подъемом ST
card_ACS_with_ST= dbc.Card(children=[
                        dbc.CardHeader("ОКС с подъемом ST", className='card_header'),
                        dbc.CardBody(html.P(id='ACS_with_ST', className='card_text'))
                        ], className='_card_'
                    )

#Карточка ОКС без подъема ST
card_ACS_without_ST=dbc.Card(children=[
                        dbc.CardHeader("ОКС без подъема ST", className='card_header'),
                        dbc.CardBody(html.P(id='ACS_without_ST', className='card_text'))
                        ], className='_card_'
                    )

#Карточка с охватом ЧКВ
card_PCI_coverage =dbc.Card(children=[
                        dbc.CardHeader("Охват ЧКВ", className='card_header'),
                        dbc.CardBody(html.P(id='PCI_coverage', className='card_text'))
                        ], className='_card_'
                    )

#Карточка летальность при ОКС
card_ACS_mort_rate=dbc.Card(children=[
                        dbc.CardHeader("Летальность при ОКС", className='card_header'),
                        dbc.CardBody(html.P(id='ACS_mort_rate', className='card_text'))
                        ], className='_card_'
                    )

#Карточка летальность при ИМ
card_MI_mortality_rate=dbc.Card(children=[
                        dbc.CardHeader("Летальность при ИМ", className='card_header'),
                        dbc.CardBody(html.P(id='MI_mortality_rate', className='card_text'))
                        ], className='_card_'
                    )

#Стопка карточек
line_of_cards= html.Div(children=[
                            card_total_ASC,
                            card_ACS_with_ST,
                            card_ACS_without_ST,
                            card_PCI_coverage,
                            card_ACS_mort_rate,
                            card_MI_mortality_rate
                                 ], className='cards_stack'
                        )

#Выбор больницы
choosing_a_hospital = html.Div(children=[
                                html.H3(children='Выберете больницу', style={'fontWeight': 550}),
                                html.P([
                                    dcc.Checklist(            
                                        ['ГОБУЗ "ЦРБ им. Гомера"', 'ГОБУЗ "ЦРБ им. Барта"', 'ГОБУЗ "ИМО"'],
                                         ['ГОБУЗ "ЦРБ им. Гомера"', 'ГОБУЗ "ЦРБ им. Барта"', 'ГОБУЗ "ИМО"'], 
                                        id='choose_a_hospital'
                                        ),
                                html.Hr()
                                        ], className='sidebar_text_style')
                                    ]
                                )
                      
#Выбор года
choosing_a_year = html.Div(children=[
                                html.H3(children='Выберете год', style={'fontWeight': 550}),
                                    html.P([
                                    dcc.RadioItems(['2022','2023', '2024'],
                                            '2022', 
                                             id='choose_a_year'
                                                ),
                                    html.Hr()
                                        ], className='sidebar_text_style')
                                    ]
                            )

#Выбор месяца
choosing_the_month = html.Div(children=[
                                    html.H3(children='Выберете месяц', style={'fontWeight': 550}),
                                    html.Div(
                                        children=[
                                            dcc.RangeSlider(
                                                min=1,
                                                max=12,
                                                step=1,
                                                value=[1, 12],
                                                marks={i: {'label': month_names[i], 'style': {'fontSize': '17px', 'color': 'black'}} for i in range(1, 13)},
                                                tooltip={"placement": "bottom", "always_visible": False},
                                                vertical=True,
                                                verticalHeight=400,
                                                id='monthly_slider'
                                            )
                                        ],
                                        className='month_slider_style'
                                    )
                                ]
                            )

#Общий элемент сайтбара 
block_sidebar= html.Div( children= [
                            choosing_a_hospital,
                            choosing_a_year, 
                            choosing_the_month
                                ], className='sidebar'
                        )

#Полный блок таблицы
table_block = html.Div( children= [
                html.Button('Показать табличные данные', id='show-table-button',className='button'),
                html.Div (id='datatable-container', className='color'),
                html.Script('''document.getElementById('show-table-button').addEventListener('click', function() {document.getElementById('datatable-container').scrollIntoView({ behavior: 'smooth' });});
                            ''')
    ])

#Гистограмма ОКС
hist_ACS= html.Div(children= [dcc.Graph(id='ACS-hist')
                            ],className='hist'
                            )
#Гистограмма пути при ОКС
hist_ACS_way= html.Div(children= [dcc.Graph(id='ACS_way')
                            ],className='hist'
                            )

hist_ACS_with_eST_risk=html.Div(children= [dcc.Graph(id='ACS_with_eST_risk')
                            ],className='hist'
                            )
#Стопка гистограмм
graphics=html.Div(children= [
                        hist_ACS,
                        hist_ACS_way,
                        hist_ACS_with_eST_risk                        
                            ]
                        )
#Объединенные блоки сайтбара и карточек
sidebar_and_cards=html.Div(children= [
                                block_sidebar,
                                line_of_cards,
                                graphics
                                    ],className='flex'
                                )