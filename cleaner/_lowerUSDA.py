import pandas as pd

# this is used for just lowering the USDA file
# should be worked into the cleaner file

df = pd.read_csv('data_cleaned/USDA_file.csv')

df['INGREDIENT'] = df['INGREDIENT'].str.lower()

df.to_csv('data_cleaned/USDA_file.csv')