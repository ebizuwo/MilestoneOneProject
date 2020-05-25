import pandas as pd

def join_df(df1, df2, on):
    return pd.merge(df1, df2, on=on, how='inner')

def master_rel():
    lat_long_rel = pd.read_csv('data_normalized/lat_long_rel.csv')

    map_rel = pd.read_csv('data_normalized/map_keys.csv')

    final_rel = join_df(lat_long_rel, map_rel, on='uid_raw_ings')

    final_rel.to_csv('data_normalized/master_rel.csv', index=False)
    # .rename(columns={'uid_lat_long': 'uid_lat_long_m', 'uid_raw_ings': 'uid_raw_ings_m',
    #                  'uid_recipe_ings': 'uid_recipe_ings_m'})
master_rel()