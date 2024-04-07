from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import json
from plotly.subplots import make_subplots

from Dashboard.Parsing_data import df  
import numpy as np


selected_hospital= ['ГОБУЗ "Боровичская ЦРБ"','ГОБУЗ "Старорусская ЦРБ"', 'ГОБУЗ "НОКБ"']
month=[1,12]
year=2023
months_dict = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
               7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}

new_df = df[(df['Hospital'].isin(selected_hospital)) & 
            (df['Date'].dt.month.isin(range(month[0], month[1] + 1))) &
            (df['Date'].dt.year == int(year))]


#ОКС без одъема ST
ACS_without_ST = new_df.loc[new_df['№ п/п'] == '47.2',['Value','Month_number']]
ACS_without_ST= ACS_without_ST.groupby(['Month_number']).sum().reset_index()
ACS_without_ST['Month_number'] = ACS_without_ST['Month_number'].replace(months_dict)


#ОКС с подъемом ST
gr_ACS_with_ST = new_df.loc[new_df['№ п/п'] == '47.1',['Value','Month_number']]
gr_ACS_with_ST = gr_ACS_with_ST.groupby(['Month_number']).sum().reset_index()
gr_ACS_with_ST['Month_number'] = gr_ACS_with_ST['Month_number'].replace(months_dict)

#Всего ОКС
total_ACS_ = new_df.loc[new_df['№ п/п'] == 47, ['Value','Month_number']]
total_ACS_= total_ACS_.groupby(['Month_number']).sum().reset_index()

# Летальность при ОКС
ACS_mort = new_df.loc[new_df['№ п/п'] == 44,['Value','Month_number']]
ACS_mort= ACS_mort.groupby(['Month_number']).sum().reset_index()
ACS_mort['Month_number'] = ACS_mort['Month_number'].replace(months_dict)
ACS_mort['mort_rate'] = ACS_mort['Value'] / total_ACS_['Value'] * 100
ACS_mort['mort_rate'] = ACS_mort['mort_rate'].map(lambda x: f'{x:.1f} %')


ACS_fig = make_subplots(specs=[[{'secondary_y': True}]])
# Добавляем гистограмму к фигуре
ACS_fig.add_trace(go.Bar(name='ОКС с подъемом ST', x=gr_ACS_with_ST['Month_number'], y=gr_ACS_with_ST['Value'],
                          text=gr_ACS_with_ST['Value'], textposition='auto', marker_color='PaleTurquoise', hoverinfo='text'),secondary_y=False)

ACS_fig.add_trace(go.Bar(name='ОКС без одъема ST', x=ACS_without_ST['Month_number'], 
                         y=ACS_without_ST['Value'], text=ACS_without_ST['Value'],textposition='auto', marker_color='SteelBlue', hoverinfo='text'), 
                         secondary_y=False)

ACS_fig.add_trace (go.Scatter(x=ACS_mort['Month_number'], y=ACS_mort['Value'], mode='lines', name='Летальность ОКС',
                              marker_color='red', text=ACS_mort['mort_rate'],
                                 textfont={'family': 'Arial', 'size': 10, 'color': 'rgb(0, 0, 0)'},
                                 textposition='top center', hoverinfo='text'),secondary_y=True)
ACS_fig.update_layout(yaxis={'visible': False, 'showticklabels': False}, yaxis2={'visible': False, 'showticklabels': False}, 
                    title={'text': '<b>Динамика количества ОКС и летальности при ОКС за выбранный год</b>',
                            'font': {'family': 'Arial', 'size': 24, 'color': 'rgb(0, 0, 0)'}, 'x': 0.5, 'y': 0.85}, 
                    plot_bgcolor='rgb(255, 255, 255)', 
                    margin={'l': 30, 'r': 0, 't': 100, 'b': 0}, 
                    legend={'x': 0.95, 'y': 0.5, 'traceorder': 'reversed', 'font': {'family': 'Arial', 'size': 14, 'color': 'Black'}, 
                            'yanchor': 'top', 'xanchor': 'left'})


ACS_fig.update_layout(barmode='stack')
ACS_fig.update_traces(textfont_size=16)

# Настройка макета
#fig.update_layout(title='Гистограмма', xaxis_title='Месяц', yaxis_title='Значение')

# Создаем объект гистограммыfig

# Отображаем гистограмму

app = Dash(__name__)

app.layout = html.Div(children=[
                        html.Div('yt b '),
                        dcc.Graph(figure=ACS_fig) 
                                 
                                                  

])



if __name__ == '__main__':
    app.run(debug=True)
