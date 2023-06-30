import pandas as pd

file1 =  pd.read_excel('./scenario_1.xlsx', sheet_name = 0)

print(file1.columns)