import pandas as pd
import datetime

# read the file
df = pd.read_csv('data/raw_ingredients/csv_market_data.csv')

def drop_columns(df, columns):
    df = df.drop(columns = columns)
    return df

def parse_lat_long(df):
    # regex find the lat longs from google line and extract
    patt = r".*\?q=(?P<lat>-\d*\.\d*|\d*\.\d*)%2C%20(?P<long>-\d*\.\d*|\d*\.\d*).*"
    dflatlong = df['GoogleLink'].str.extract(patt)
    # join with existing dataframe and return
    df = df.join(dflatlong)
    return df

def split_products_list(df):
    df['Product_List'] = df['Products'].str.split(';')
    return df

def write_file(df, f):
    df.to_csv(f, index=False)

def explode_product_list(df):
    return df.explode('Product_List')

# drop columns
df = drop_columns(df, ['Unnamed: 0', 'Address', 'Schedule'])

# parse out lat long
df = parse_lat_long(df)

# drop NaNs
df = df.dropna()

# extract products into a list in one column
df = split_products_list(df)

# drop other columns
df = drop_columns(df, ['GoogleLink', 'Products'])

# explode product list
df = explode_product_list(df)

# write to file
write_file(df, f'data_cleaned/market_data_cleaned_{datetime.datetime.now()}.csv')


