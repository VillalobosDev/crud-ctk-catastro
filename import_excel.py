import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

connection_url = URL.create('sqlite', database='regdb.db')

engine = create_engine(connection_url)

excel_file = r'C:\Github\crud-ctk-catastro\crud-ctk-catastro\file.xlsx'
df_excel = pd.read_excel(excel_file, sheet_name=None)
import pandas as pd

# Load the Excel file (sheet_name=None loads all sheets into a dictionary of DataFrames)
df_excel = pd.read_excel(excel_file, sheet_name=None)

# Replace NaN with empty string or other placeholder value in all sheets
df_excel_cleaned = {sheet_name: sheet_data.fillna('') for sheet_name, sheet_data in df_excel.items()}

# Now df_excel_cleaned contains the cleaned data where NaN values are replaced
print(df_excel_cleaned)
