from dash import  html, dash_table, dcc
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from Parsing_data import df


#Главная рассчетная функция
def calculations (selected_hospital, month, year, n_clicks):

            months_dict = {1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
               7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'}

#Подготовка данных
            new_df = df[(df['Hospital'].isin(selected_hospital)) & 
                        (df['Date'].dt.month.isin(range(month[0], month[1] + 1))) &
                        (df['Date'].dt.year == int(year))]

#Основная таблица
            table = dash_table.DataTable(data=new_df.to_dict('records'),
                                        page_size=15,
                                        style_data={
                                            'whiteSpace': 'normal',
                                            'backgroundColor': '#BEEFFF', 
                                            'height': 'auto'
                                                    },
                                        style_header={
                                            'backgroundColor': '#BEEFFF',
                                            'fontWeight': 'bold' 
                                                    }
                                        )
# Всего ОКС
            total_ACS = new_df.loc[new_df['№ п/п'] == 47, 'Value'].sum()

# Кол-во ОКС с подъемом ST
            ACS_with_ST = new_df.loc[new_df['№ п/п'] == '47.1','Value'].sum()

# Кол-во ОКС без подъема ST
            ACS_without_ST = new_df.loc[new_df['№ п/п'] == '47.2','Value'].sum()

# Охват ЧКВ
            PTCA_cnt = new_df.loc[new_df['№ п/п'] == '39.1','Value'].sum()
            PCI_coverage =  f'{round((PTCA_cnt / total_ACS)*100, 1)} %' if total_ACS > 0 else 0

# Летальность при ОКС
            ACS_mort = new_df.loc[new_df['№ п/п'] == 44,'Value'].sum()
            ACS_mort_rate = f'{round((ACS_mort / total_ACS)*100, 1)} %' if total_ACS > 0 else 0

# Летальность при ИМ
            IM_mort = new_df.loc[new_df['№ п/п'] == 48,'Value'].sum()
            total_IM = new_df.loc[new_df['№ п/п'] == 49,'Value'].sum()
            MI_mortality_rate = f'{round((IM_mort / total_IM)*100, 1)} %' if total_IM > 0 else 0

#Блок для работы кнопки, окрывающей таблицу
            if n_clicks is None:
                block_table = []

            elif n_clicks % 2 != 0: 
                block_table=html.Div(children=[
                    html.Div('Табличные данные', className='heading_table'),
                    html.Div(table,className='b_table')])
            else:
                block_table = []                
#Расчеты для гистограммы
#ОКС без одъема ST
            gr_ACS_without_ST = new_df.loc[new_df['№ п/п'] == '47.2',['Value','Month_number']]
            gr_ACS_without_ST= gr_ACS_without_ST.groupby(['Month_number']).sum().reset_index()
            gr_ACS_without_ST['Month_number'] = gr_ACS_without_ST['Month_number'].replace(months_dict)

#ОКС с подъемом ST
            gr_ACS_with_ST = new_df.loc[new_df['№ п/п'] == '47.1',['Value','Month_number']]
            gr_ACS_with_ST = gr_ACS_with_ST.groupby(['Month_number']).sum().reset_index()
            gr_ACS_with_ST['Month_number'] = gr_ACS_with_ST['Month_number'].replace(months_dict)

#Всего ОКС
            gr_total_ACS_ = new_df.loc[new_df['№ п/п'] == 47, ['Value','Month_number']]
            gr_total_ACS_= gr_total_ACS_.groupby(['Month_number']).sum().reset_index()

# Летальность при ОКС
            gr_ACS_mort = new_df.loc[new_df['№ п/п'] == 44,['Value','Month_number']]
            gr_ACS_mort= gr_ACS_mort.groupby(['Month_number']).sum().reset_index()
            gr_ACS_mort['Month_number'] = gr_ACS_mort['Month_number'].replace(months_dict)
            gr_ACS_mort['mort_rate'] = gr_ACS_mort['Value'] / gr_total_ACS_['Value'] * 100
            gr_ACS_mort['mort_rate'] = gr_ACS_mort['mort_rate'].map(lambda x: f'{x:.1f} %')


            ACS_fig = make_subplots(specs=[[{'secondary_y': True}]]) #Позволяет наложить несколько осей Y на один график

# Добавление гистограммы для ОКС с подъемом ST
            ACS_fig.add_trace(go.Bar(
                    name='ОКС с подъемом ST',
                    x=gr_ACS_with_ST['Month_number'],
                    y=gr_ACS_with_ST['Value'],
                    text=gr_ACS_with_ST['Value'],
                    textposition='auto',
                    marker_color='rgb(15, 130, 240)',
                    hoverinfo='text'
                ), secondary_y=False)

# Добавление гистограммы для ОКС без подъема ST
            ACS_fig.add_trace(go.Bar(
                name='ОКС без подъема ST',
                x=gr_ACS_without_ST['Month_number'],
                y=gr_ACS_without_ST['Value'],
                text=gr_ACS_without_ST['Value'],
                textposition='auto',
                marker_color='rgb(100, 170, 240)',
                hoverinfo='text'
            ), secondary_y=False)

# Добавление линии для летальности ОКС
            ACS_fig.add_trace(go.Scatter(
                x=gr_ACS_mort['Month_number'],
                y=gr_ACS_mort['Value'],
                mode='lines',
                name='Летальность ОКС',
                marker_color='red',
                text=gr_ACS_mort['mort_rate'],
                textfont={'family': 'Arial', 'size': 10, 'color': 'rgb(0, 0, 0)'},
                textposition='top center',
                hoverinfo='text'
            ), secondary_y=True)

# Обновление макета графика
            ACS_fig.update_layout(
                yaxis={'visible': False, 'showticklabels': False},
                yaxis2={'visible': False, 'showticklabels': False},
                title={'text': '<b>Динамика количества и летальности при ОКС</b>',
                    'font': {'family': 'Arial', 'size': 24, 'color': 'rgb(0, 0, 0)'},
                    'x': 0.5, 'y': 0.85},
                plot_bgcolor='rgb(190, 239, 255)',
                paper_bgcolor='rgb(190, 239, 255)', 
                margin={'l': 30, 'r': 0, 't': 100, 'b': 0},
                legend={'x': 0.95, 'y': 0.5, 'traceorder': 'reversed',
                        'font': {'family': 'Arial', 'size': 14, 'color': 'Black'},
                        'yanchor': 'top', 'xanchor': 'left'}
            )

# Обновление стиля гистограмм
            ACS_fig.update_layout(barmode='stack')
            ACS_fig.update_traces(textfont_size=18)
        
            return total_ACS, ACS_with_ST, ACS_without_ST, PCI_coverage,ACS_mort_rate, MI_mortality_rate, block_table, ACS_fig

