import pandas as pd
from dash import Dash, html, dcc, dash_table, callback, Output, Input

#import plotly.express as px
#from plotly.subplots import make_subplots
#import plotly.graph_objects as go

from Parsing_data import df
from Style import b_table

def calculations (selected_hospital, month, year ):
        #Фильтр
            #Основная таблица
            t_year=[int (x) for x in year]
            new_df = df[(df['Hospital'].isin(selected_hospital)) & (df['Month'].isin(range(month[0], month [1]+1))) & (df['Date'].dt.year.isin (t_year))]
            table= dash_table.DataTable(style_data=b_table,
                            data=new_df.to_dict('records'), 
                            page_size=15
                            )
            # Всего ОКС
            total_ACS = df.loc[(df['№ п/п'] == 47) &
                            (df['Date'].dt.year.isin (t_year)) &
                            (df['Date'].dt.month.isin(month)) &
                            (df['Hospital'].isin(selected_hospital)), 'Value'].sum()
            #Кол-во ОКС с подъемом ST
            ACS_with_ST = df.loc[(df['№ п/п'] == '47.1') &
                            (df['Date'].dt.year.isin (t_year)) &
                            (df['Date'].dt.month.isin(range(month[0], month [1]+1))) &
                            (df['Hospital'].isin(selected_hospital))].shape[0]
            #Кол-во ОКС без подъема ST
            ACS_without_ST = df.loc[(df['№ п/п'] == '47.2') &
                            (df['Date'].dt.year.isin (t_year)) &
                            (df['Date'].dt.month.isin(range(month[0], month [1]+1))) &
                            (df['Hospital'].isin(selected_hospital))].shape[0]

            return total_ACS, ACS_with_ST, ACS_without_ST, table
