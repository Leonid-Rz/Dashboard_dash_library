import pandas as pd
import numpy as np
from pathlib import Path

pd.set_option('display.max.columns', None)
pd.set_option('display.max.rows', None)


excel_file = '_Мониторинг_Сахалин.xlsx'
df = pd.read_excel(excel_file)
print (df.ilock[0:5])
# Заполнение свободных ячеек рандомными цифрами
#for row_index in range(df.shape[0]):
#    for col_index in range(df.shape[1]):
#        if pd.isnull(df.iloc[row_index, col_index]):  # Проверяем, является ли ячейка пустой
#            df.iloc[row_index, col_index] = np.random.randint(0, 100)  # Заполняем ячейку случайным числом от 0 до 99

# Сохранение изменений в новый файл Excel
#new_excel_file = "новый_файл.xlsx"
#df.to_excel(new_excel_file, index=False)
