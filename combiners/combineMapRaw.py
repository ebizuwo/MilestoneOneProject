import pandas as pd
from functools import reduce


# def join_df(df1,df2,df3):
#     dfs = [df1, df2, df3]
#     reduce(lambda left, right: pd.merge(left, right, on='name'), dfs)
#
#     return df1.merge(df2, how='inner', on=)

def join_df(df1, df2, on):
    try:
        return pd.merge(df1, df2, on=on, how='left')
    except Exception as e:
        print(e)

def combineMapRaw():
    df_map = pd.read_csv('data_combined/classified_recipe_raw.csv')
    df_raw = pd.read_csv('data_cleaned/raw_ingredients.csv')
    df_rec = pd.read_csv('data_cleaned/recipe_ingredients.csv')

    # stupid column names be more careful next time
    try:
        df_raw = df_raw.drop(columns=['Unnamed: 0'])
    except Exception as e:
        print(e)

    try:
        df_raw = df_raw.rename(columns={'ingredients':'raw_ingredient'})
    except Exception as e:
        print(e)

    print(df_raw.columns)
    recipe_map_df = join_df(df_rec, df_map, on='recipe_ingredients')


    master_combined = join_df(df_raw, recipe_map_df, on='raw_ingredient')

    try:
        master_combined = master_combined.drop(columns=['Unnamed: 0'])
    except Exception as e:
        print(e)

    master_combined.to_csv('data_combined/master_data.csv')



combineMapRaw()