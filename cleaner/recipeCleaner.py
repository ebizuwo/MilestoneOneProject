import pandas as pd
import us
import holidays
import numpy as np
import modules.valueSelector as vs

# object to collect columns
class column_collector(object):
    columns = []
    def __init__(self, f):
        self.f = f()
        try:
            self.columns.extend(self.f)
        except Exception as e:
            print(e)

    def __call__(self):
        pass


def drop_the_columns(df, cols, ind=None):
    if ind:
        df = df.drop(index=ind)
    if cols:
        for c in cols:
            try:
                df = df.drop(columns=c)
            except Exception as e:
                print(e)
                continue
    return df


# These are way we create a bunch of columns to drop
# need different ways of creating the columns
# this is a nifty way to track them
@column_collector
def create_states():
    states = [s.name.lower() for s in us.states.STATES]
    return states

@column_collector
def create_cities():
    return None

@column_collector
def create_holidays():
    us_holidays = holidays.UnitedStates(years=2020).values()
    return [h.lower() for h in us_holidays]



def user_selection(df):
    user_selected_columns = vs.ValueDropper(df.columns).initiate_selection()
    df = drop_the_columns(df, user_selected_columns)
    @column_collector
    def create_selector():
        return user_selected_columns
    return df


def write_file(df, f):
    df.to_csv(f)


def make_recipe_column(df):
    def apply_recipe_search(x):
        m = x==1
        return x[np.where(m,True,False)].index.to_list()

    df['recipe_ingredients'] = df.apply(apply_recipe_search, axis=1)
    return df


def explode_ingredients(df):
    return df.explode('recipe_ingredients')


def recipe_cleaner():
    # read csv
    df = pd.read_csv('data/recipe/epirecipes/epi_r.csv')
    original_columns = df.columns

    # main script

    # start by dropping columns collected in columns
    # this will select user input
    df = drop_the_columns(df, column_collector.columns)

    # lets do user selection dropping
    df = user_selection(df)

    # let now create a list of ingredients for each recipe
    df = make_recipe_column(df)

    # get columns we care about
    df = df[['title', 'recipe_ingredients']]

    # explode the dataframe now
    df = explode_ingredients(df)

    # write df to the file
    write_file(df, 'data_cleaned/recipe_ingredients.csv')





