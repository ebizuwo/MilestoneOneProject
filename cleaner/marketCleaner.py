import pandas as pd
import datetime



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

def market_cleaner():
    # read the file
    df = pd.read_csv('data/raw_ingredients/csv_market_data.csv')

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

    # lower everything because its good practice
    df['Product_List'] = df['Product_List'].str.lower()

    # remove leading spaces
    df['Product_List'] = df['Product_List'].str.strip()

    # write to file
    write_file(df, f'data_cleaned/market_data_cleaned.csv')


