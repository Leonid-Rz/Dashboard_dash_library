import pandas as pd
from pathlib import Path

#Установка параметров pandas для выведения без ограничений всех столбцов и строк
pd.set_option('display.max.columns', None)
pd.set_option('display.max.rows', None)

#Создание списка объеков типа Path с путями до файлов типа .xls из папки Data
p = Path(r'./Data') 
file_list = list(p.glob('*.xls'))
   
#Создаем шаблон для DataFrame на основе шапки первой таблицы из списка
file = file_list[0]
df = pd.read_excel(file, engine='openpyxl') 
columns = [col.replace('\n', ' ') for col in list(df.iloc[5])] 
columns.insert(0, 'Source') 
df = pd.DataFrame(columns=columns)

#Создаем DataFrame с данными из всех таблиц, опираясь на полученный выше шаблон
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

#Переводим данные DataFrame в длинный формат
id_cols = ['Source', '№ п/п', 'Целевые показатели оценки эффективности реализации мероприятий', 'Единицы измерения', 'Периодичность представления'] 
val_cols = [col for col in df.columns if col.startswith('Фактическое')] 
df = pd.melt(df, id_vars=id_cols, value_vars=val_cols, var_name='Attribute', value_name='Value_NI').dropna(axis='index', subset=['Value_NI']).reset_index(drop=True)

#Чистим данные в DataFrame
df['Value_NI'].replace({'Х': 0, '': 0}, inplace=True)   
df['Value_NI'].fillna(value=0, inplace=True)            
df['Source'] = df['Source'].str.replace(' ', '_')    

#Создание новых столбцов с корректной датой - Date и Date_prev
df[['Source_1', 'Source_2', 'Year', 'Hospital', 'Source_5', 'Source_6', 'Source_7', 'Source_8']] = df['Source'].str.split('_', expand=True)
    #В новые столбцы записываем данные из 'Source', разбитые по знаку '_'
df['Year'] = df['Year'].astype('int')
df['Month'] = 0
df['Day'] = 1

for index, row in df.iterrows():
    for j in range(1, 13):
        if str(j) in row['Attribute']: 
            df.at[index, 'Month'] = j #Находим месяц через совпадение в записях столбца 'Attribute' и вставляем совпавшее 
    df.at[index, 'Year'] = row['Year'] + 2000 #Корректируем год

df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']], dayfirst=True) 
df['Date_prev'] = df['Date'] - pd.DateOffset(months=1)

df.drop(columns=['Source', 'Year', 'Month', 'Day', 'Attribute', 'Source_1', 'Source_2',
                 'Source_5', 'Source_6', 'Source_7', 'Source_8'], inplace=True) #Чистим от лишних столбцов 
df = df[['Hospital', 'Date', 'Date_prev', 'Целевые показатели оценки эффективности реализации мероприятий',
         '№ п/п', 'Единицы измерения', 'Периодичность представления', 'Value_NI']]


#Объединение DataFrame с копией DataFrame для привязки предыдущего периода
df_prev = df[['Hospital', 'Date', 'Целевые показатели оценки эффективности реализации мероприятий',
         '№ п/п', 'Value_NI']].copy() #Создали копию df, взяв только нужные столбцы 
df_prev.rename({'Value_NI':'Value_prev', 'Date':'Date_prev'}, axis='columns', inplace=True)
df = df.merge(df_prev, how='left', on=['Hospital', 'Date_prev', 'Целевые показатели оценки эффективности реализации мероприятий', '№ п/п'])
df['Value_prev'] = df['Value_prev'].fillna(value=0) 

hosp_dict = {'Гомера':'ГОБУЗ "ЦРБ им. Гомера"', 'Барта':'ГОБУЗ "ЦРБ им. Барта"', 'ИМО':'ГОБУЗ "ИМО"'} 
df['Hospital'].replace(to_replace=hosp_dict, inplace=True)

#Создание столбца фактического значения'
def create_value(row):
    if row['Периодичность представления'] != '1 раз в месяц':
        val = row['Value_NI']
    elif row['Date'].month == 1:
        val = row['Value_NI']
    else:
        val = row['Value_NI'] - row['Value_prev']
    return val

#Создаем новый столбец в df и заполняет его значениями из функции create_value
df['Value'] = df.apply(create_value, axis=1) 
df['Month_number'] = df['Date'].dt.month

#Сохранение полученного DataFrame в виде таблички, если мы в главной ветке
if __name__ == '__main__': 
    #df.to_excel(r'Мониторинг_Спрингфилд.xlsx')
    print(df.info())