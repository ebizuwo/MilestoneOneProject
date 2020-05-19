import pandas as pd
import csv

def read_csv(file):
    df = pd.read_csv(file)
    return df


df = read_csv('data/raw_ingredients/USDA_file.csv')
print(df.head(10))