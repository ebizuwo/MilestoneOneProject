
import geopandas as gpd
import pandas as pd
import numpy as np
import json
import folium


def chloropleth():
    county_geo = 'data/location/US_counties.geojson'

    df = gpd.read_file(county_geo, driver='GeoJSON')

    # Set to contiguous United States to limit range of mean distances and widen distribution for visualization
    alpha = df[~df['STATEFP'].isin(['02','15','60','66','69','72','78'])].reset_index()
    

    #creating normalized dataframes
    COUNTY_COORD = alpha[['NAME','INTPTLAT','INTPTLON','GEOID']].reset_index().rename(columns = {'index':'uid_lat_long','GEOID':'geo_id','INTPTLAT':'lat','INTPTLON':'long'})

    #setting as float
    COUNTY_COORD.lat = COUNTY_COORD.lat.astype(float)
    COUNTY_COORD.long = COUNTY_COORD.long.astype(float)

    COUNTY_COORD[:,'mean_distance'] = COUNTY_COORD.apply(lambda x: avg_distance(x.lat, x.long), axis = 1)

    # Create Choloropleth map from data
    # Initialize the map to contiguous states:
    m = folium.Map(location=[37, -102], zoom_start=5)
    # Add the color for the chloropleth:
    m.choropleth(geo_data=county_geo,
                         fill_color='YlGn', fill_opacity=0.5, line_opacity=0.5,
                         data = COUNTY_COORD,
                         key_on='feature.properties.GEOID',
                         columns = ['geo_id', 'mean_distance']
                         ) 
    m.save('data_output/counties_mean_distance.html')


