

import pandas as pd
from pathlib import Path

pd.set_option('display.max.columns', None)
pd.set_option('display.max.rows', None)

p = Path(r'./Data') 
file_list = [x for x in p.iterdir() if str(x).endswith('.xls')]


file = file_list[0]
df = pd.read_excel(file, engine='openpyxl') 
columns = [col.replace('\n', ' ') for col in list(df.iloc[5])] 
columns.insert(0, 'Source')  
df = pd.DataFrame(columns=columns)

for file in file_list: 
    df_f = pd.read_excel(file, engine='openpyxl') 
    columns = [col.replace('\n', ' ') for col in list(df_f.iloc[5])]
    df_f.columns = columns 
    df_f = df_f[7:].reset_index(drop=True)
    source = str(file)[str(file).rfind('\\') + 1:].replace('.xls', '') 
    df_f['Source'] = source
    df_f.dropna(axis='index', 
                subset=['Целевые показатели оценки эффективности реализации мероприятий'],
                inplace=True) 
    df = pd.concat([df, df_f],ignore_index=True)  

id_cols = ['Source', '№ п/п', 'Целевые показатели оценки эффективности реализации мероприятий', 'Единицы измерения', 'Периодичность представления'] 
val_cols = [col for col in df.columns if col.startswith('Фактическое')] 
df = pd.melt(df, id_vars=id_cols, value_vars=val_cols, var_name='Attribute', value_name='Value_NI').dropna(axis='index', subset=['Value_NI']).reset_index(drop=True)
   
df['Value_NI'].replace({'Х': 0, '': 0}, inplace=True)   
df['Value_NI'].fillna(value=0, inplace=True)            
df['Source'] = df['Source'].str.replace(' ', '_')     


df[['Source_1', 'Source_2', 'Year', 'Hospital', 'Source_5', 'Source_6', 'Source_7', 'Source_8']] = df['Source'].str.split('_', expand=True)
df['Year'] = df['Year'].astype('int')
df['Month'] = 0
df['Day'] = 1

for index, row in df.iterrows():
    for j in range(1, 13):
        if str(j) in row['Attribute']: 
            df.at[index, 'Month'] = j 
    df.at[index, 'Year'] = row['Year'] + 2000 

df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']], dayfirst=True) 
df['Date_prev'] = df['Date'] - pd.DateOffset(months=1) 

df.drop(columns=['Source', 'Year', 'Day', 'Attribute', 'Source_1', 'Source_2',
                 'Source_5', 'Source_6', 'Source_7', 'Source_8'], inplace=True) 


df = df[['Hospital', 'Date', 'Month', 'Date_prev', 'Целевые показатели оценки эффективности реализации мероприятий',
         '№ п/п', 'Единицы измерения', 'Периодичность представления', 'Value_NI']]

df_prev = df[['Hospital', 'Date', 'Целевые показатели оценки эффективности реализации мероприятий',
         '№ п/п', 'Value_NI']].copy() 
df_prev.rename({'Value_NI':'Value_prev', 'Date':'Date_prev'}, axis='columns', inplace=True)
df = df.merge(df_prev, how='left', on=['Hospital', 'Date_prev', 'Целевые показатели оценки эффективности реализации мероприятий', '№ п/п'])
df['Value_prev'] = df['Value_prev'].fillna(value=0) 

hosp_dict = {'Боровичская':'ГОБУЗ "Боровичская ЦРБ"', 'Старорусская':'ГОБУЗ "Старорусская ЦРБ"', 'НОКБ':'ГОБУЗ "НОКБ"'} 
df['Hospital'].replace(to_replace=hosp_dict, inplace=True)


def create_value(row):
    if row['Периодичность представления'] != '1 раз в месяц':
        val = row['Value_NI']
    elif row['Date'].month == 1:
        val = row['Value_NI']
    else:
        val = row['Value_NI'] - row['Value_prev']
    return val


df['Value'] = df.apply(create_value, axis=1) 

print (df.iloc[0:5])

if __name__ == '__main__': 
    df.to_excel(r'Мониторинг_Новгород.xlsx')



            html.Div(
            children=[total_ACS_card, ACS_with_elevation_ST_card, ACS_without_elevation_ST_card],
            style={'display': 'inline-block', 'vertical-align': 'top', 'width': '15%', 'left': 0}),
    








def choose_hospital_ASC(year, month, input_hospital):
    month_range = range(month[0], month[1])
    # Всего ОКС
    total_ACS = df.loc[(df['№ п/п'] == 47) &
                       (df['Date'].dt.to_period('Y') == year) &
                       (df['Date'].dt.month.isin(month_range)) &
                       (df['Hospital'].isin(input_hospital)), 'Value'].sum()

    return total_ACS, ACS_with_elevation_ST, ACS_without_elevation_ST, ACS_fig, f'{PCI_coverage:.1%}', \
           f'{ACS_mortality_rate:.1%}', f'{MI_mortality_rate:.1%}', MI_fig, ACS_path_funnel_fig, \
           f'Умерших: {int(cnt_deaths_ACS_with_eST)}', f'Общая летальность при ОКСпST: {ACS_with_eST_mortality_rate:.1%}', \
           f'Летальность идеального пути: {ACS_with_eST_ideal_path_mortality_rate:.1%}', \
           f'Доля умерших без ЧКВ, АКШ и ТЛТ: {ACS_with_eST_without_revasc_deaths_part:.1%}', ACS_with_eST_risk_fig, \
           f'Охват ЧКВ: {ACS_without_eST_high_risk_PTCA_coverage:.1%}', \
           f'Летальность: {ACS_without_eST_high_risk_mortality_rate:.1%}', \
           f'Охват ЧКВ: {ACS_without_eST_low_risk_PTCA_coverage:.1%}', \
           f'Летальность: {ACS_without_eST_high_risk_mortality_rate:.1%}', Shock_fig, \
           f'Кол-во ОКС с шоком: {int(cnt_shock)}', f'Охват ЧКВ: {shock_PTCA_coverage:.1%}', \
           f'Летальность при шоке: {shock_mortality_rate:.1%}', \
           f'Доля пациентов с шоком среди всех умерших при ОКС {part_shock_for_deaths:.1%}'


total_ACS_card = dbc.Card(
    children=[
        dbc.CardHeader("Всего ОКС", className='information_card_header_1'),
        dbc.CardBody(html.P(className="card_text_1", id='total_ASC'))
    ],
    className='information_card_1')
app.layout = html.Div(
    #style={'backgroundColor': colors['background']},
    children=[
        sidebar,
        tabs_navigator_offcanvas,
        content
    ]
)


@callback(
    Output(component_id='total_ASC', component_property='children'),
    Output(component_id='cnt_ACS_with_elevation_ST', component_property='children'),
    Output(component_id='cnt_ACS_without_elevation_ST', component_property='children'),
    Output(component_id='ACS_bar', component_property='figure'),
    Output(component_id='PCI_coverage', component_property='children'),
    Output(component_id='ACS_mortality_rate', component_property='children'),
    Output(component_id='MI_mortality_rate', component_property='children'),
    Output(component_id='MI_bar', component_property='figure'),
    Output(component_id='ACS_path_funnel', component_property='figure'),
    Output(component_id='count_deaths_ACS_with_eST', component_property='children'),
    Output(component_id='mortality_rate_ACS_with_eST', component_property='children'),
    Output(component_id='mortality_rate_ACS_with_eST_ideal_path', component_property='children'),
    Output(component_id='part_deaths_ACS_with_eST_without_revasc', component_property='children'),
    Output(component_id='ACS_without_eST_risk', component_property='figure'),
    Output(component_id='PTCA_coverage_ACS_without_eST_high_risk', component_property='children'),
    Output(component_id='mortality_rate_ACS_without_eST_high_risk', component_property='children'),
    Output(component_id='PTCA_coverage_ACS_without_eST_low_risk', component_property='children'),
    Output(component_id='mortality_rate_ACS_without_eST_low_risk', component_property='children'),
    Output(component_id='Shock_bar', component_property='figure'),
    Output(component_id='count_shock', component_property='children'),
    Output(component_id='PTCA_coverage_for_shock', component_property='children'),
    Output(component_id='mortality_rate_shock', component_property='children'),
    Output(component_id='part_shock_for_deaths', component_property='children'),
    Input(component_id='year_choice', component_property='value'),
    Input(component_id='month_choice', component_property='value'),
    Input(component_id='hospital_choice', component_property='value')
)
def intermediate_function(*args, **kwargs):
    return choose_hospital_ASC(*args, **kwargs)


@callback(
    Output(component_id='Tabs_navigator', component_property='is_open'),
    Input(component_id='Tabs_navigator_open_button', component_property='n_clicks'),
    [State("Tabs_navigator", "is_open")],
)
def open_tabs_navigator(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Development server
# if __name__ == '__main__':

year_choice_card = dbc.Card(
    children=[
        dbc.CardHeader('Выберите год отчета', className='card-filter_header_1'),
        dbc.CardBody(dcc.RadioItems(options=['2022', '2023', '2024'], value='2023', id='year_choice'))
    ],
    className='card-filter_1')
