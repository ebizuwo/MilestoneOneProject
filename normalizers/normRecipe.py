import pandas as pd

def recipe_name_uid(df):
    rnames = set(df['title'])
    df_ = pd.DataFrame({
        'title' : [x for x in rnames],
        'uid_title': range(len(rnames))
    })
    return df_

def recipe_ing_uid(df):
    ings = set(df['recipe_ingredients'])
    df_ = pd.DataFrame({
        'recipe_ingredients': [x for x in ings],
        'uid_recipe_ings': range(len(ings))

    })
    return df_

def join_df(df1, df2, on):
    return pd.merge(df1, df2, on=on, how='inner')

def norm_recipe():
    # recipes data rows 71583
    df_recipes = pd.read_csv('data_cleaned/recipe_ingredients.csv')
    # print(df_recipes)

    # recipes with unique id 17736 rows
    df_recipe_uid = recipe_name_uid(df_recipes).rename(columns={'uid_title': 'uid_recipe_title'})
    df_recipe_uid.rename(columns={'title':'recipe_title','uid_title': 'uid_recipe_title'}).to_csv('data_normalized/recipe_title.csv',index=False)

    # recipe ingredients with unique id 278 rows
    df_recipe_ings_uid = recipe_ing_uid(df_recipes)
    df_recipe_ings_uid.to_csv('data_normalized/recipe_ings.csv', index=False)

    # silly join sequence
    # join recipes onto recipe ings uid 71583 rows
    df_recipe_uid_recipes = join_df(df_recipe_uid, df_recipes, on='title')
    print(df_recipe_uid_recipes)

    # join ing uid on previous 71583
    df_final_recipe_ing_uid = join_df(df_recipe_uid_recipes, df_recipe_ings_uid, on='recipe_ingredients')

    # write the important stuff to normalized files

    df_final_recipe_ing_uid[['uid_recipe_ings', 'uid_recipe_title']].to_csv('data_normalized/recipe_rel.csv', index=False)


norm_recipe()