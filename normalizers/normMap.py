import pandas as pd


def join_df(df1, df2, on):
    return pd.merge(df1, df2, on=on, how='inner')

def norm_map():
    df_map = pd.read_csv('data_combined/classified_recipe_raw.csv')
    df_raw = pd.read_csv('data_normalized/raw_ings.csv')
    df_rec = pd.read_csv('data_normalized/recipe_ings.csv', usecols=['recipe_ingredients', 'uid_recipe_ings'])

    df1 = join_df(df_map, df_raw, on='raw_ingredient')
    # print(df1)

    df2 = join_df(df1, df_rec, on='recipe_ingredients').drop_duplicates()

    df2[['uid_raw_ings', 'uid_recipe_ings']].to_csv('data_normalized/map_keys.csv', index=False)

norm_map()