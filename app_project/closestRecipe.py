import sqlite3
import sqlalchemy
import pandas as pd
from haversine import haversine, Unit
import pgeocode


class ClosestRecipe:
    #globals
    ranked_recipes = None
    ranked_recipe_ingredients = None
    lat_long = None
    zip_ = None
    def __init__(self):
        self.conn = None
        try:
            self.conn = sqlite3.connect('farmtoface.db')
            self.conn.create_function('haversine', 2, self.udf_haversine)
        except Exception as e:
            self.conn = sqlite3.connect('app_project/farmtoface.db')
            self.conn.create_function('haversine', 2, self.udf_haversine)
            print(e)



    def udf_haversine(self, lat, long):
        inglatlong = (lat, long)
        lat_long = self.lat_long
        assert lat_long, 'lat long not set in class'
        try:
            return haversine(inglatlong, lat_long, Unit.MILES)
        except Exception as e:
            print(e)


    def zip_lookup_lat_long(self, zip_):
        # using a library called pgeocode
        nomi = pgeocode.Nominatim('US')
        geoinfo = nomi.query_postal_code(zip_)
        lat = geoinfo.loc['latitude']
        long = geoinfo.loc['longitude']
        return lat, long

    def recipe_rank_zip(self, zip_):
        self.zip_ = zip_
        self.lat_long = self.zip_lookup_lat_long(zip_)
        query = """
            SELECT avg_dist, recipe_title as recipe, rt.uid_recipe_title
            FROM (SELECT AVG(ing_distance) as avg_dist, mind.uid_recipe_title
                    FROM (SELECT closest_ing.mindist as ing_distance, rel.uid_recipe_title
                            FROM(SELECT m.uid_raw_ings, MIN(dist.distance) as mindist
                                    FROM master_rel as m
                                    INNER JOIN (SELECT uid_lat_long, haversine(lat,long) as distance FROM lat_long) as dist
                                    ON m.uid_lat_long = dist.uid_lat_long
                                    GROUP BY m.uid_raw_ings) as closest_ing
                            INNER JOIN recipe_rel as rel 
                            ON closest_ing.uid_raw_ings = rel.uid_recipe_ings) as mind
                    GROUP BY mind.uid_recipe_title
                    ORDER BY avg_dist ASC) as avgd
            INNER JOIN  recipe_title as rt
            ON avgd.uid_recipe_title = rt.uid_recipe_title
            ORDER BY avg_dist ASC 
        """

        df = pd.read_sql(query, self.conn)
        self.ranked_recipes = df
        return df

    def recipe_rank_ings_zip(self, zip_):
        def manipulate_df(df):
            df['uid_recipe_ings'] = df['uid_recipe_ings'].str.split(',')
            df = df.explode('uid_recipe_ings').astype(int)
            dflatlong = self.get_lat_long()
            dfrecipeing = self.get_recipe_ing()
            dfreciperel = self.get_recipe_rel()
            df = pd.merge(df, dflatlong, on='uid_lat_long', how='inner')
            df = pd.merge(df, dfrecipeing, on='uid_recipe_ings')
            df = pd.merge(df, dfreciperel, on='uid_recipe_ings')
            return df

        self.lat_long = self.zip_lookup_lat_long(zip_)
        query = """
            SELECT dist.uid_lat_long, MIN(dist.distance) as distance, GROUP_CONCAT(DISTINCT(m.uid_recipe_ings)) as uid_recipe_ings
            FROM master_rel as m
            INNER JOIN (SELECT uid_lat_long, haversine(lat,long) as distance FROM lat_long) as dist
            ON m.uid_lat_long = dist.uid_lat_long
            GROUP BY m.uid_raw_ings
            """

        # cursor.execute(query)
        # df = pd.DataFrame(cursor.fetchall())
        # df.columns = ['uid_lat_long', 'distance', 'uid_recipe_ings']
        # df = manipulate_df(df)
        # print(df)
        df = pd.read_sql(query, self.conn)
        df = manipulate_df(df)
        self.ranked_recipe_ingredients = df
        return df

    def recipe_rank_avg_lat_long(self, lat_long):
        self.lat_long = lat_long
        query = """
            SELECT AVG(avg_dist)
            FROM (SELECT AVG(ing_distance) as avg_dist, mind.uid_recipe_title
                    FROM (SELECT closest_ing.mindist as ing_distance, rel.uid_recipe_title
                            FROM(SELECT m.uid_raw_ings, MIN(dist.distance) as mindist
                                    FROM master_rel as m
                                    INNER JOIN (SELECT uid_lat_long, haversine(lat,long) as distance FROM lat_long) as dist
                                    ON m.uid_lat_long = dist.uid_lat_long
                                    GROUP BY m.uid_raw_ings) as closest_ing
                            INNER JOIN recipe_rel as rel 
                            ON closest_ing.uid_raw_ings = rel.uid_recipe_ings) as mind
                    GROUP BY mind.uid_recipe_title
                    ORDER BY avg_dist ASC) as avgd
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        avg = cursor.fetchall()
        return avg


    def get_combined_rank_ings(self):
        return pd.merge(self.ranked_recipes, self.ranked_recipe_ingredients, on='uid_recipe_title')

    def get_recipe_ing(self):
        query = """
            SELECT *
            FROM recipe_ings
        """
        return pd.read_sql(query, self.conn)

    def get_lat_long(self):
        return pd.read_sql("SELECT * FROM lat_long", self.conn)

    def get_recipe_rel(self):
        return pd.read_sql("SELECT * FROM recipe_rel", self.conn)

    def connect_sqlite(self, conn):
        self.conn = conn
        return self







