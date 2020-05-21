from urllib.error import HTTPError
import requests
import zipcodes
import pandas
import pprint
import csv
import json
from zips import zips
import time
import re

#pretty printing the json its just easier this way
pp = pprint.PrettyPrinter(indent=4)

## This defines a variable for getting zipcodes
get_zips_url = "https://api.zip-codes.com/ZipCodesAPI.svc/1.0/GetAllZipCodes?state=&country=US&key=DEMOAPIKEY"

# zip farm data file
zipFarmDataFile = 'data/zip_farm_data.csv'

#market data file
marketDataFile = 'data_cleaned/market_details_data.csv'

#json market data file
jsonMarketDataFile = 'data_cleaned/json_market_data.json'

def construct_lat_lng_url(lat, lng):
    return f"http://search.ams.usda.gov/farmersmarkets/v1/data.svc/locSearch?lat={lat}&lng={lng}"

def construct_zip_url(zip):
    base = "http://search.ams.usda.gov/farmersmarkets/v1/data.svc/zipSearch?zip="
    return f"{base}{zip}"

def construct_market_detail_url(id):
    base = "http://search.ams.usda.gov/farmersmarkets/v1/data.svc/mktDetail?id="
    return f"{base}{id}"

def get_request(url):
    """
    This is a generic get request and response setup could be expanded on for more error handling
    :param url:
    :return: response to the get request
    """
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Python 3.6
    except Exception as err:
        print(f'Other error occurred: {err}')  # Python 3.6
    finally:
        pass
        # print('Success!')

def get_zips():
    """
    This Queries the demo API for zip codes. Not sure how great this list is but it should be all the
    Zips available in the US.
    No parameters
    Outputs a list of zipcodes to iterate through
    """
    return get_request(get_zips_url).json()



#Functions for Writing data to file
def write_csv_header(filename, header):
    with open(filename, 'w') as fp:
        csvwr = csv.writer(fp)
        csvwr.writerow(header)

def write_csv_line(filename, data):
    with open(filename, 'w') as fp:
        csvwr = csv.writer(fp)
        for l in data:
            csvwr.writerow(l)

def write_json_to_file(jsond, filename):
    with open(filename, 'w+') as fp:
        json.dump(jsond, fp)


#Functions for converting json data to csv
def json_convert_csv(json):

    pass



#This section handles doing the requests for zips
def get_farmers_data_by_zip(zip):
    url = construct_zip_url(zip)
    resp = get_request(url)
    if resp:
        return resp.json()
    else:
        return None


def get_farmers_data_by_zip_generator():
    zips = get_zips()
    for zip in zips:
        zipFarmData = get_farmers_data_by_zip(zip)
        yield zipFarmData



#This section handles doing the request for lat lng
def get_farmers_data_by_lat_lng(lat, lng):
    url = construct_lat_lng_url(lat, lng)
    resp = get_request(url)
    if resp:
        return resp.json()
    else:
        return None

def get_farmers_data_by_lat_lng_generator():
    pass

#This section handles doing the requests by id and such
def parse_ids_from_zips_resp(resp):
    ids = [r['id'] for r in resp['results']]
    return ids

def get_farmers_details_by_id(id):
    url = construct_market_detail_url(id)
    resp = get_request(url)
    if resp:
        return resp.json()
    else:
        return None

def get_farmers_details_by_id_generator(ids):
    for id in ids:
        yield get_farmers_details_by_id(id).json()



#Start initiates the first steps in the process and starts all the good stuff


def cascade(zip):


    zipFarmData = get_farmers_data_by_zip(zip)

    ids = parse_ids_from_zips_resp(zipFarmData)

    idMarketData = get_farmers_details_by_id_generator(ids)



#was building a whole bunch of complicated request write stuff with generators
#totally not needed here

def generator_start_request_cascade():
    #TODO: Make these into functions

    # clears the zip_farm_data.csv file for writing later down the stack
    f_zipFarmDataFile = open(zipFarmDataFile, "w+")
    f_zipFarmDataFile.close()

    # clears the zip_farm_data.csv file for writing later down the stack
    f_marketDataFile = open(marketDataFile, "w+")
    f_marketDataFile.close()

    # get all the zips first request
    zips = get_zips()
    # loop through the zips in a generator so we dont go to far
    for zip in zips:
        yield cascade(zip)


#going to make a function to determine which ids to remove
def calc_diff_ids(curr_ids, new_ids):
    pass

def calc_diff_names(curr_names, new_ids):
    pass

def calc_diff_latlng(curr_latlng, new_ltlng):
    pass

def do_some_parsing(farm):
    def parse_name(name):
        regex = r'\d*[.]\d* '
        s = re.sub(regex,'', name)
        if s:
            return s
        else:
            return None

    def parse_id(id):
        #may not be needed here
        return id

    id = parse_id(farm['id'])
    name = parse_name(farm['marketname'])

    return {'id': id, 'marketname': name}



#start the requesting and writing process
def simple_request_store():
    # zips = get_zips()
    # print(zips)
    t1 = time.time()
    total = len(zips)
    count = 0
    farmers_markets = []
    farms = set()
    for zip in zips:
        zipFarmData = get_farmers_data_by_zip(zip)
        count += 1

        #printing for tracking
        print(f"working on zip = {zip} "
              f"Number {count} of {total}")

        #let's determine if we need to loop through the markets
        if zipFarmData:
            #current list of response ids for the zip
            #let's clean em up because there is some sort of dupe situation

            parsed_farm = set()
            for farm in zipFarmData['results']:
                pf = do_some_parsing(farm)
                if pf:
                    parsed_farm.add(tuple(pf.items()))

            #set difference to get out what is not already in the farms
            diff_farms = parsed_farm - farms
            for f in diff_farms:
                farms.add(f)

            #counters
            totalf = len(diff_farms)
            countf = 0

            # loop through whats left
            if len(diff_farms) > 0:
                for market in diff_farms:
                    countf+=1
                    print(f"working on market {countf} of {totalf} in {zip}")

                    id = market[0][1]
                    farmDetails = get_farmers_details_by_id(id)
                    if farmDetails:
                        farmers_markets.append(farmDetails)
                    else:
                        pass
            else:
                print(f'no new farms for zip = {zip}')

    print(f"writing to file now because lets not request everything again")
    write_json_to_file(farmers_markets, jsonMarketDataFile)
    t2 = time.time()
    print(f"done in {t2-t1}")


simple_request_store()