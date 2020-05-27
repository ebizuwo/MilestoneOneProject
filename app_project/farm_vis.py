
import geopandas as gpd
import pandas as pd
import numpy as np
import json
import folium
import seaborn as sns
import matplotlib.pyplot as plt
from closestRecipe import ClosestRecipe
class farm_vis:
    def __init__(self):
        pass
    
    def chloropleth():
        cr = ClosestRecipe()
        county_geo = '../data/location/US_counties.geojson'

        df = gpd.read_file(county_geo, driver='GeoJSON')

        # Set to contiguous United States to limit range of mean distances and widen distribution for visualization
        alpha = df[~df['STATEFP'].isin(['02','15','60','66','69','72','78'])].reset_index()


        #creating normalized dataframes
        COUNTY_COORD = alpha[['NAME','INTPTLAT','INTPTLON','GEOID']].reset_index().rename(columns = {'index':'uid_lat_long','GEOID':'geo_id','INTPTLAT':'lat','INTPTLON':'long'})

        #setting as float
        COUNTY_COORD.lat = COUNTY_COORD.lat.astype(float)
        COUNTY_COORD.long = COUNTY_COORD.long.astype(float)

        COUNTY_COORD.loc[:,'mean_distance'] = COUNTY_COORD.apply(lambda x: cr.recipe_rank_avg_lat_long((x.lat,x.long))[0][0], axis = 1)

        #Create Choloropleth map from data
        # Initialize the map to contiguous states:
        m = folium.Map(location=[37, -102], zoom_start=5)
        # Add the color for the chloropleth:
        m.choropleth(geo_data=county_geo,
                             fill_color='YlGn', fill_opacity=0.5, line_opacity=0.5,
                             data = COUNTY_COORD,
                             key_on='feature.properties.GEOID',
                             columns = ['geo_id', 'mean_distance']
                             ) 
        m.save('../data/counties_mean_distance.html')


    def dist_plot(self,x,y):
        #x = recipe_frame
        #y = current_index
        density = (y+1)/len(x)
        mcdf = sns.kdeplot(x['mean_score'], cumulative=True, shade=True, color="b").set(
            xlabel='recipe average distance', ylabel='% recipes closer')
        plt.plot([y, y], [0, density])
