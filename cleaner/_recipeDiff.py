import pandas as pd
import json

df = pd.read_csv('data/recipe/epirecipes/epi_r.csv')
original_columns = set(df.columns)


# kept_columns = []
with open('data_classified/classified.json', 'r') as fp:
    json_ = json.load(fp)
    kept_columns = set([k for k in json_.keys()])
    fp.close()
    with open('data_selected/selectedDrop.json', 'w') as fp_:
        json.dump(list(original_columns - kept_columns), fp_)
        fp_.close()
    with open('data_selected/selectedKeep.json', 'w') as fp_1:
        json.dump(list(original_columns & kept_columns), fp_1)
        fp_1.close()