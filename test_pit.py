from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import json

from Dashboard.Parsing_data import df  
import numpy as np


selected_hospital= ['ГОБУЗ "Боровичская ЦРБ"','ГОБУЗ "Старорусская ЦРБ"', 'ГОБУЗ "НОКБ"']
month=[1,12]
year=2022

new_df = df[(df['Hospital'].isin(selected_hospital)) & 
                (df['Date'].dt.month.isin(range(month[0], month[1] + 1))) &
                (df['Date'].dt.year == int(year))]
ACS = new_df[new_df['№ п/п'] == 47][['Value','Month_number']]

fig = go.Figure()

# Добавляем гистограмму к фигуре
fig.add_trace(go.Histogram(x=ACS['Month_number'], y=ACS['Value']))

# Настройка макета
fig.update_layout(title='Гистограмма', xaxis_title='Месяц', yaxis_title='Значение')

# Создаем объект гистограммы

# Отображаем гистограмму

app = Dash(__name__)

app.layout = html.Div(children=[
                        html.Div('yt b '),
                        dcc.Graph(figure=fig) 
                                 
                                                  

])



if __name__ == '__main__':
    app.run(debug=True)
