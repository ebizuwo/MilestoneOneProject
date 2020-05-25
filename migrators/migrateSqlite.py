import sqlite3
import sqlalchemy
import pandas as pd

# create database
conn = sqlite3.connect('sqlite_db/farmtoface.db')  # You can create a new database by changing the name within the quotes
c = conn.cursor()

# create the tables we need
# lat_long
# raw_ings
# recipe_ings
# recipe_title
# master_rel
# recipe_rel

try:
    c.execute('''DROP TABLE lat_long''')
    c.execute('''DROP TABLE raw_ings''')
    c.execute('''DROP TABLE recipe_ings''')
    c.execute('''DROP TABLE recipe_title''')
    c.execute('''DROP TABLE master_rel''')
    c.execute('''DROP TABLE recipe_rel''')
except Exception as e:
    print(e)



# create the tables


c.execute('''CREATE TABLE lat_long
            (
            uid_lat_long INTEGER PRIMARY KEY,
            lat float,
            long float)''')
conn.commit()


c.execute('''CREATE TABLE raw_ings
            (
            uid_raw_ings INTEGER PRIMARY KEY,
            raw_ingredient text)''')
conn.commit()


c.execute('''CREATE TABLE recipe_ings
             (
             uid_recipe_ings INTEGER PRIMARY KEY,
             recipe_ingredients text)''')
conn.commit()


c.execute('''CREATE TABLE recipe_title
             (
             uid_recipe_title INTEGER PRIMARY KEY,
             recipe_title text )''')
conn.commit()


c.execute('''CREATE TABLE master_rel
             (
             uid_raw_ings INTEGER,
             uid_lat_long INTEGER,
             uid_recipe_ings INTEGER,
             FOREIGN KEY (uid_raw_ings) references raw_ings(uid_raw_ings),
             FOREIGN KEY (uid_recipe_ings) references recipe_ings(uid_recipe_ings),
             FOREIGN KEY (uid_lat_long) references lat_long(uid_lat_long))''')
conn.commit()

c.execute('''CREATE TABLE recipe_rel
             (
             uid_recipe_ings INTEGER,
             uid_recipe_title INTEGER,
             FOREIGN KEY (uid_recipe_ings) references recipe_ings(uid_recipe_ings),
             FOREIGN KEY (uid_recipe_title) references recipe_title(uid_recipe_title))''')
conn.commit()


# now add the csv to the tables pandas can do this yooooo

def sql_objs():

    lat_long = 'data_normalized/lat_long.csv'
    raw_ings = 'data_normalized/raw_ings.csv'
    recipe_ings = 'data_normalized/recipe_ings.csv'
    recipe_title = 'data_normalized/recipe_title.csv'
    master_rel = 'data_normalized/master_rel.csv'
    recipe_rel = 'data_normalized/recipe_rel.csv'

    files = [lat_long, raw_ings, recipe_ings, recipe_title, master_rel, recipe_rel]
    tables = ['lat_long', 'raw_ings', 'recipe_ings', 'recipe_title', 'master_rel', 'recipe_rel']

    sql_objs = zip(files,tables)
    return sql_objs


def insert_csv(sqlobj):
    df = pd.read_csv(sqlobj[0])
    df.to_sql(sqlobj[1], conn, if_exists='replace', index=False)


def make_migrations():
    for s in sql_objs():
        insert_csv(s)