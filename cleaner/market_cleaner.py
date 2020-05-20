import pandas as pd

# read the file
df = pd.read_csv('data/raw_ingredients/csv_market_data.csv')

def parse_lat_long(link):
    pass

def drop_columns(df):
    df = df.drop(index=[0,1,4])
    return df

print(df.columns)
df = drop_columns(df)
print(df.columns)
