import pandas as pd
import numpy as np
import modules.valueSelector as vs
import re

# globals
raw_ingredients = 'data_cleaned/raw_ingredients.csv'
recipe_ingredients = 'data_cleaned/recipe_ingredients.csv'
# output
recipes_mapped_raw = 'data_combined/recipes_mapped_raw.csv'


class MapRecRawDF():
    rec_col = 'recipe_ingredients'
    raw_col = 'raw_ingredient'
    dataframe = ''
    raw_rec_intersection = ''
    def __init__(self, set_rec, set_raw):
        self.set_rec = set_rec
        self.set_raw = set_raw
        self.rec_arr = self.set_to_arr(self.set_rec)
        self.get_intersection()
        self.construct_df()
        self.map_by_contains()

    def construct_df(self):
        # there is logic here to go ahead and set things that match
        self.dataframe = pd.DataFrame({
            self.rec_col: self.rec_arr,
            self.raw_col: [x if x in self.raw_rec_intersection else np.nan for x in self.rec_arr]
        }).set_index(self.rec_col)

    def set_to_arr(self, set_rec):
        # make an array and also drop the pseudo nan
        arr_list = [x for x in set_rec if (x != 'nan' and x != np.nan)]
        return arr_list

    def add_map(self, rec_raw_map):
        rec, raw = rec_raw_map
        self.dataframe.loc[rec, self.raw_col] = raw
        # assert self.dataframe.loc[rec, self.raw_col] == raw, f"did not successfully add mapping {(rec, raw)}"


    def add_map_list(self, rec_raw_map_list):
        try:
            for m, v in rec_raw_map_list:
                if not self.is_populated(m):
                    self.add_map(rec_raw_map_list)
        except Exception as e:
            print(e)

    def is_populated(self, rec):
        if rec:
            try:
                if self.dataframe.loc[rec, self.raw_col]:
                    return True
                else:
                    return False
            except Exception as e:
                print(e)


    def map_by_contains(self):
        def regex_search(rec, raw):
            return re.search(fr"{rec}", raw)
        rec = self.set_rec
        raw = self.set_raw
        for rec_ing in rec:
            if not self.is_populated(rec_ing):
                for raw_ing in raw:
                    if str(rec_ing) in raw_ing:
                        self.add_map((rec_ing, raw_ing))
                    if regex_search(rec_ing, raw_ing):
                        self.add_map((rec_ing, raw_ing))

    def get_items_to_classify(self):
        # return the index where the raw ingredient is not matched
        s = self.dataframe[self.dataframe.isnull().any(1)].index.to_list()
        return s


    def get_intersection(self):
        intersection = self.set_raw & self.set_raw
        self.raw_rec_intersection = intersection
        return intersection


def combineRawRecipe():

    recipe_ingredients_column = 'recipe_ingredients'
    raw_ingredients_column = 'ingredients'

    # read in the dataframe (could be costly on mem)
    df_raw = pd.read_csv(raw_ingredients)
    df_rec = pd.read_csv(recipe_ingredients)

    # all unique values for the ingredients
    set_raw = set(df_raw[raw_ingredients_column].unique())
    set_rec = set(df_rec[recipe_ingredients_column].unique())

    # construct the mapping
    map_rec_raw_obj = MapRecRawDF(set_rec, set_raw)

    # lets select values that we may need to keep things that are
    # occupied in the map
    items_to_classify = map_rec_raw_obj.get_items_to_classify()
    categories = list(set_raw)

    # lets fire up the classifer
    classifier = vs.ValueClassifier(items_to_classify, categories)
    val_dict, map_store = classifier.initiate_classifier(map_rec_raw_obj)

    # write to file now
    map_store.dataframe.to_csv('data_combined/classified_recipe_raw.csv')

    print('ALL DONE')


