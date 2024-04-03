import pandas as pd
from dash import Dash, html, dcc, dash_table, callback, Output, Input

#import plotly.express as px
#from plotly.subplots import make_subplots
#import plotly.graph_objects as go

from Parsing_data import df

b_table = {'whiteSpace': 'normal',
        'backgroundColor': 'white', 
        'height': 'auto'}


def calculations (selected_hospital, month, year ):
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
                                            'height': 'auto'},
                                        style_header={
                                            'backgroundColor': '#BEEFFF',
                                            'fontWeight': 'bold'  
    }
                                        )
            # Всего ОКС
            total_ACS =  new_df.loc[new_df['№ п/п'] == 47, 'Value'].sum()

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

            return total_ACS, ACS_with_ST, ACS_without_ST, PCI_coverage,ACS_mort_rate, MI_mortality_rate, table 
