
import geopandas as gpd

def county_shape():
    df = gpd.read_file('data/location/US_counties.geojson', driver='GeoJSON')

    #extracting key information to allow for normalization
    alpha = df[~df['STATEFP'].isin(['02','15','60','66','69','72','78'])].reset_index()
    beta = alpha[['NAME','INTPTLAT','INTPTLON','GEOID']].reset_index().rename(columns = {'index':'LL_index'})
    gamma = beta.groupby('NAME').count().reset_index().reset_index().rename(columns = {'index':'uid_county'})
    delta = beta.merge(gamma, left_on = 'NAME',right_on = 'NAME')

    #creating normalized dataframes
    COUNTY_NAMES = gamma[['uid_county','NAME']].rename(columns = {'NAME':'county_name'})
    COUNTY_COORD = beta[['LL_index','INTPTLAT','INTPTLON']].rename(columns = {'LL_index':'uid_lat_long','INTPTLAT':'lat','INTPTLON':'long'})
    COUNTY_GEOID = beta[['LL_index','GEOID']].rename(columns = {'LL_index':'uid_lat_long','GEOID':'geo_id'})
    COORD_NAME = delta[['LL_index_x','uid_county']].rename(columns = {'LL_index_x':'uid_lat_long'}).sort_values('uid_lat_long') 

    #setting as float
    COUNTY_COORD.lat = COUNTY_COORD.lat.astype(float)
    COUNTY_COORD.long = COUNTY_COORD.long.astype(float)
    COUNTY_GEOID.geo_id = COUNTY_GEOID.geo_id.astype(int)

    #export all to csv
    COUNTY_COORD.to_csv('data_normalized/county_lat_long.csv',index=False)
    COUNTY_NAMES.to_csv('data_normalized/county_names.csv',index=False)
    COORD_NAME.to_csv('data_normalized/county_rel.csv',index=False)
    COUNTY_GEOID.to_csv('data_normalized/county_geo_id.csv',index=False)

county_shape()
