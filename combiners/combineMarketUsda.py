import pandas as pd

desired_col_names = ['lat', 'long', 'ingredients']


def read_usda(f, usecols):
    return pd.read_csv(f, usecols=usecols)

def read_csv(f):
    return pd.read_csv(f)


def concat_dataframes(frames):
    return pd.concat(frames)


def write_csv(df, f):
    df.to_csv(f)


def combineMarketUsda():

    # read in the dataframe
    df_u = read_usda('data_cleaned/USDA_file.csv', ['LAT', 'LON', 'INGREDIENT'])

    # rename the columns
    df_u.columns = desired_col_names

    # df for market data
    df_m = read_csv('data_cleaned/market_data_cleaned.csv')

    # rename the columns
    df_m.columns = desired_col_names

    # concat the two
    df = concat_dataframes([df_u, df_m])

    # write to file
    write_csv(df, 'data_cleaned/raw_ingredients.csv')






