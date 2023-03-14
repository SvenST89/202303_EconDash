# To make web requests at the ECB SDMX 2.1 RESTful web service
import requests

# Standard libs for data manipulation
import pandas as pd
import numpy as np
import io
from datetime import date
import re
from config.api import MY_API_KEY
import logging

#========================================================================================================================================#

def get_index_table():
    entrypoint="https://financialmodelingprep.com/api/v3/"
    headers = {'Accept': 'application/json'}
    my_api_key=MY_API_KEY
    requestUrl='https://financialmodelingprep.com/api/v3/quotes/index?apikey='+my_api_key
    response = requests.get(requestUrl)#, headers=headers)
    assert response.status_code == 200, f"Expected response code 200, got {response.status_code} for {requestUrl}. Check again your url!"
    # use the .json() method offered by 'requests' package: https://datagy.io/python-requests-json/
    response_list=response.json()
    # make dataframe from list
    table=pd.DataFrame(response_list)[['symbol', 'name']]
    return table

def get_profile_data(ticker, json_entry='beta', entry_point='profile'):
    my_api_key=MY_API_KEY
    entrypoint_profile="https://financialmodelingprep.com/api/v3/profile/"
    entrypoint_shares="https://financialmodelingprep.com/api/v4/shares_float?symbol="
    headers = {'Accept': 'application/json'}
    
    # get company beta value from FMP
    # For the extract function I used the code of this colleague instead of working it out on my own (sorry! too lazy!)
    # https://python.plainenglish.io/extracting-specific-keys-values-from-a-messed-up-json-file-python-dfb671482681
    def extract(data, keys):
        out = []
        queue = [data]
        while len(queue) > 0:
            current = queue.pop(0)
            if type(current) == dict:
                for key in keys:
                    if key in current:
                        out.append({key:current[key]})
            
                for val in current.values():
                    if type(val) in [list, dict]:
                        queue.append(val)
            elif type(current) == list:
                queue.extend(current)
        return out
    # Now make request to FMP API
    if entry_point == 'profile':
        requestUrl= entrypoint_profile + ticker + "?" +  "apikey=" + my_api_key
        response = requests.get(requestUrl)#, headers=headers)
        assert response.status_code == 200, f"Expected response code 200, got {response.status_code} for {requestUrl}. Check again your url!"
    elif entry_point == 'shares':
        requestUrl= entrypoint_shares + ticker +  "&apikey=" + my_api_key
        response = requests.get(requestUrl)#, headers=headers)
        assert response.status_code == 200, f"Expected response code 200, got {response.status_code} for {requestUrl}. Check again your url!"
    else:
        print("You´ve chosen an entrypoint that this function does not deliver anything from. Either choose 'profile' for profile data or 'shares' for data on the company`s shares.")
    # use the .json() method offered by 'requests' package: https://datagy.io/python-requests-json/
    response_list=response.json()
    entry=extract(response_list, [json_entry])
    entry=entry[0][json_entry]
    return entry

def stock_pctchange(ticker, json_entry='1D'):
    my_api_key=MY_API_KEY
    entrypoint_profile="https://financialmodelingprep.com/api/v3/stock-price-change/"
    headers = {'Accept': 'application/json'}
    
    # get company beta value from FMP
    # For the extract function I used the code of this colleague instead of working it out on my own (sorry! too lazy!)
    # https://python.plainenglish.io/extracting-specific-keys-values-from-a-messed-up-json-file-python-dfb671482681
    def extract(data, keys):
        out = []
        queue = [data]
        while len(queue) > 0:
            current = queue.pop(0)
            if type(current) == dict:
                for key in keys:
                    if key in current:
                        out.append({key:current[key]})
            
                for val in current.values():
                    if type(val) in [list, dict]:
                        queue.append(val)
            elif type(current) == list:
                queue.extend(current)
        return out
    # Now make request to FMP API
    requestUrl= entrypoint_profile + ticker + "?" +  "apikey=" + my_api_key
    response = requests.get(requestUrl)#, headers=headers)
    assert response.status_code == 200, f"Expected response code 200, got {response.status_code} for {requestUrl}. Check again your url!"
    # use the .json() method offered by 'requests' package: https://datagy.io/python-requests-json/
    response_list=response.json()
    entry=extract(response_list, [json_entry])
    entry=entry[0][json_entry]
    return entry