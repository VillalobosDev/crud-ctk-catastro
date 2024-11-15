import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create('sqlite', database='regdb.db')

engine = create_engine(connection_url)

excel_file = r'C:\Github\crud-ctk-catastro\crud-ctk-catastro\file.xlsx'
df_excel = pd.read_excel(excel_file, sheet_name=None)

df_excel_cleaned = {sheet_name: sheet_data.dropna(how='all') 
                    for sheet_name, sheet_data in df_excel.items()}

print(df_excel)