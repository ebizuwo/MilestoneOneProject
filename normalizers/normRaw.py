import pandas as pd


def lat_long_uniques(df):
    tpls = set(list(zip(df['lat'], df['long'])))
    # create new df
    df_ = pd.DataFrame({
        'lat':[l for l,lo in tpls],
        'long':[lo for l,lo in tpls],
        'uid_lat_long':range(0, len(tpls))
    })
    return df_

def ing_uniques(df):
    ings = set(list(df['ingredients']))
    df_ = pd.DataFrame({
        'ingredients':[x for x in ings],
        'uid_ing':range(0, len(ings))
    })
    return df_

def join_df(df1, df2, on):
    return pd.merge(df1, df2, on=on, how='inner')


def norm_raw():
    # raw ingredients 1651970 rows initially after drop duplicates = 292298
    raw = pd.read_csv('data_cleaned/raw_ingredients.csv', usecols=['lat', 'long', 'ingredients']).drop_duplicates()

    # unique lat longs 8925 rows
    df_lat_long = lat_long_uniques(raw)

    # write to csv
    df_lat_long.to_csv('data_normalized/lat_long.csv', index=False)

    # generate uid for ingredients 224 rows
    df_ing = ing_uniques(raw)

    # join raw onto lat longs 292298
    df_lat_long_raw = join_df(df_lat_long, raw, on=['lat', 'long'])

    # join df_ing onto df_lat_long_raw 292298
    df_uid = join_df(df_lat_long_raw, df_ing, on='ingredients')

    # these are the dataframes we care about
    # 292298 rows
    df_lat_long_uid_ing = df_uid[['uid_ing', 'uid_lat_long']].drop_duplicates()
    # 224 rows
    df_ing_uid = df_uid[['uid_ing', 'ingredients']].drop_duplicates()

    # write to files
    df_lat_long_uid_ing.rename(columns={'uid_ing': 'uid_raw_ings'}).to_csv('data_normalized/lat_long_rel.csv', index=False)
    df_ing_uid.rename(columns={'uid_ing': 'uid_raw_ings', 'ingredients':'raw_ingredient'}).to_csv('data_normalized/raw_ings.csv', index=False)

norm_raw()






