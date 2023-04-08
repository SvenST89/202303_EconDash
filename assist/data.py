# To make web requests at the ECB SDMX 2.1 RESTful web service
import requests

# For use of the ECB API
#from sdw_api import SDW_API

# Standard libs for data manipulation
import pandas as pd
import numpy as np
import io
import datetime
from datetime import date
from datetime import timedelta as td
import re
import itertools

import logging
import sys

logger=logging.getLogger()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(lineno)s - %(levelname)s - %(message)s')
logger.setLevel(logging.DEBUG)

# set logging handler in file
fileHandler=logging.FileHandler(filename="log/func.log", mode='w')
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)

# set logging handler in console
consoleHandler=logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(formatter)
consoleHandler.setLevel(logging.INFO)
logger.addHandler(consoleHandler)
#===================================================#

# This script will retrieve yield curve time series data from the ECB SDM 2.1 RESTful web service through making a http get request. 
# Basically, it is like a function replicating the sdw_api python package from the ECB, but is more flexible in the sense that it 
# does not throw an error for the yield curve data across different maturities, which was the case for the api package.

def get_ecb_data(keys_list, time_series='yields', actual=True):
    #=================================================================#
    # Note on the methodology
    # re.findall() function returns all non-overlapping matches of a pattern in a string. The function returns all the findings as a list. The search happens from left to right.

    # --- (\w+): The \w matches a "word character"— something alphanumeric or an underscore;
    #            the + matches one or more of these; and the parentheses group and store them in the first capturing group.
    # -------\.: It stops when it sees a fullstop '.', which needs to be escaped with '\'.
    # 
    # Hence, this method splits the time series key into its constituent parts and stores them in variables.
    # As for the keyRemainder we join, so to say, the 'remainder' of the time series key after having isolated the database identifier (e.g. YC, for 'Yield Curve' dataflow) by putting '.' regex in the front of '(\w+)'.
    # We do this iteratively for each time series key in a for loop.
    # ================================================================#
    # Entrypoint for the ECB SDMX 2.1 RESTful web service
    entrypoint="https://sdw-wsrest.ecb.europa.eu/service/data/"

    # Pandas dataframe list
    pd_list=[]

    if actual:
        logger.info(f"Retrieving most recent data for the ECB time series on {time_series}.")
        for i in keys_list:
            #===============================================================
            # store time series (ts) key components in a list
            keyComponent_list = re.findall(r"(\w+)\.",i)
            # access the database identifier, which is the very first component at index 0
            db_id = keyComponent_list[0]
            # remainder of key components
            keyRemainder = '.'.join(re.findall(r"\.(\w+)",i))
            # merge the request url
            requestUrl= entrypoint + db_id+ "/" + keyRemainder + "?format=genericdata"
            #--------------------------------------------------------------
    
            # Set parameters for http request get method
            today = date.today()        # get the date of today
            start = today-td(days=5)
            start = start.strftime("%Y-%m-%d")
            today_formatted = today.strftime("%Y-%m-%d") # format the date as a string 2020-10-31
            parameters = {
            'startPeriod': start,  # Start date of the time series, e.g. '2019-12-01'
            'endPeriod': today_formatted     # End of the time series
            }
            #--------------------------------------------------------------
        
            # Make the HTTP get request for each url
            response = requests.get(requestUrl, params=parameters, headers={'Accept': 'text/csv'})
            #logger.info('Expected response code 200: {}'.format(if {response.status_code} != 200 "Something did not work with your http-request for {requestUrl}. Check your url again, please!" else "The request for {requestUrl} was fine. I received {response.status_code}."))#assert response.status_code == 200, f"Expected response code 200, got {response.status_code} for {requestUrl}. Check again your url!"
            #--------------------------------------------------------------

            # Read the response as a file into a Pandas Dataframe
            ecb_df = pd.read_csv(io.StringIO(response.text))
            # Create a new DataFrame called 'ir_ts'; isolating Time Period and Observation Value only.
            ecb_ts = ecb_df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
            #--------------------------------------------------------------

            if time_series=='yields':
                # Identify the dataframe with its residual maturity; if >9 years it will be 10, 11, etc.
                # so prepare string variable as the column name
                name_num=keyRemainder[29]
                name_freq=keyRemainder[30]
                name_short=name_num+name_freq
                if name_freq!='Y' and name_freq!='M':
                    name_long=name_short #+'Y'
                    ecb_ts.rename(columns={'OBS_VALUE':name_long}, inplace=True)
                elif name_freq=='Y':
                    name_long = name_short[0]
                    ecb_ts.rename(columns={'OBS_VALUE':name_long}, inplace=True)
                else:
                    ecb_ts.rename(columns={'OBS_VALUE':'M' + name_short[0]}, inplace=True)
            else:
                continue
            #--------------------------------------------------------------
        
            pd_list.append(ecb_ts)
            #===============================================================
        
        # Now concatenate each individual yield curve dataframe from the list of dataframes,
        # collected in the loop, into one single dataframe
        df=pd.concat(pd_list, axis=1)
        df_rev=df.drop("TIME_PERIOD", axis=1).T.reset_index()
        df_rev.rename(columns={'index':'Maturity', 0:'Value'}, inplace=True)
        df_rev['date']=start
        df_rev=df_rev.set_index('date', inplace=False)
        df_rev_sorted=df_rev.sort_values('Maturity')
        df_m=df_rev_sorted.iloc[30:33, :]
        df_y=df_rev_sorted.iloc[0:30, :]
        df_y['Maturity']=pd.to_numeric(df_y['Maturity'])
        df_y_sort=df_y.sort_values("Maturity")
        df_final=pd.concat([df_m, df_y_sort])
        v=0.25
        for i in ['M3', 'M6', 'M9']:
            df_final.loc[df_final['Maturity']==i, ['Maturity']]=v
            v=v+0.25
    
    else:
        for i in keys_list:
            #===============================================================
            # store time series (ts) key components in a list
            keyComponent_list = re.findall(r"(\w+)\.",i)
            # access the database identifier, which is the very first component at index 0
            db_id = keyComponent_list[0]
            # remainder of key components
            keyRemainder = '.'.join(re.findall(r"\.(\w+)",i))
            # merge the request url
            requestUrl= entrypoint + db_id+ "/" + keyRemainder + "?format=genericdata"
            #--------------------------------------------------------------
    
            # Set parameters for http request get method
            today = date.today()        # get the date of today
            start = today-td(days=730)
            start = start.strftime("%Y-%m-%d")
            today_formatted = today.strftime("%Y-%m-%d") # format the date as a string 2020-10-31
            parameters = {
            'startPeriod': start,  # Start date of the time series, e.g. '2019-12-01'
            'endPeriod': today_formatted     # End of the time series
            }
            #--------------------------------------------------------------
            logger.info(f"Retrieving data for the ECB time series on {time_series} starting from {start}.")
            # Make the HTTP get request for each url
            response = requests.get(requestUrl, params=parameters, headers={'Accept': 'text/csv'})
            #assert response.status_code == 200, f"Expected response code 200, got {response.status_code} for {requestUrl}. Check again your url!"
            logger.info(f"Response Code for key {i}: {response.status_code}.")
            #--------------------------------------------------------------

            # Read the response as a file into a Pandas Dataframe
            ecb_df = pd.read_csv(io.StringIO(response.text))
            # Create a new DataFrame called 'ir_ts'; isolating Time Period and Observation Value only.
            ecb_ts = ecb_df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
            logger.info(f'Columns of retrieved ECB time series dataframe: {ecb_ts.columns}.\n Shape of dataframe: {ecb_ts.shape}.')
            #--------------------------------------------------------------

            if time_series=='yields':
                # Identify the dataframe with its residual maturity; if >9 years it will be 10, 11, etc.
                # so prepare string variable as the column name
                name_num=keyRemainder[29]
                name_freq=keyRemainder[30]
                name_short=name_num+name_freq
                if name_freq!='Y' and name_freq!='M':
                    name_long=name_short + 'Y'
                    ecb_ts.rename(columns={'OBS_VALUE':name_long}, inplace=True)
                else:
                    ecb_ts.rename(columns={'OBS_VALUE':name_short}, inplace=True)
            else:
                continue
            #--------------------------------------------------------------
        
            # 'TIME_PERIOD' was of type 'object' (as can be seen in yc_df.info). Convert it to datetime first
            ecb_ts['TIME_PERIOD'] = pd.to_datetime(ecb_ts['TIME_PERIOD'])
            # Set 'TIME_PERIOD' to be the index
            ecb = ecb_ts.set_index('TIME_PERIOD')
            # Append individual dataframe to pd_list
            pd_list.append(ecb)
            #===============================================================
        
        # Now concatenate each individual yield curve dataframe from the list of dataframes,
        # collected in the loop, into one single dataframe
        df_final=pd.concat(pd_list, axis=1)
    return df_final

def get_other_data(keys_list, country_list=["DE", "FR", "I8"]):
    entrypoint="https://sdw-wsrest.ecb.europa.eu/service/data/"

    # Pandas dataframe list
    pd_list=[]

    for i, j in zip(keys_list, country_list):
        #===============================================================
        # match country/region identifier
        z=re.search(j, i).group()
        # store time series (ts) key components in a list
        keyComponent_list = re.findall(r"(\w+)\.",i)
        # access the database identifier, which is the very first component at index 0
        db_id = keyComponent_list[0]
        # remainder of key components
        keyRemainder = '.'.join(re.findall(r"\.(\w+)",i))
        # merge the request url
        requestUrl= entrypoint + db_id+ "/" + keyRemainder + "?format=genericdata"
        #--------------------------------------------------------------
    
        # Set parameters for http request get method
        today = date.today()        # get the date of today
        start = today-td(days=730)
        start = start.strftime("%Y-%m-%d")
        today_formatted = today.strftime("%Y-%m-%d") # format the date as a string 2020-10-31
        parameters = {
        'startPeriod': start,  # Start date of the time series, e.g. '2019-12-01'
        'endPeriod': today_formatted     # End of the time series
        }
        #--------------------------------------------------------------
        #logger.info(f"Retrieving data for the ECB time series on {time_series} starting from {start}.")
        # Make the HTTP get request for each url
        response = requests.get(requestUrl, params=parameters, headers={'Accept': 'text/csv'})
        #assert response.status_code == 200, f"Expected response code 200, got {response.status_code} for {requestUrl}. Check again your url!"
        logger.info(f"Response Code for key {i}: {response.status_code}.")
        #--------------------------------------------------------------

        # Read the response as a file into a Pandas Dataframe
        ecb_df = pd.read_csv(io.StringIO(response.text))
        # Create a new DataFrame called 'ir_ts'; isolating Time Period and Observation Value only.
        ecb_ts = ecb_df.filter(['TIME_PERIOD', 'OBS_VALUE'], axis=1)
        logger.info(f'Columns of retrieved ECB time series dataframe: {ecb_ts.columns}.\n Shape of dataframe: {ecb_ts.shape}.')
        ecb_ts.rename(columns={'OBS_VALUE': z}, inplace=True)
        #--------------------------------------------------------------
        
        # 'TIME_PERIOD' was of type 'object' (as can be seen in yc_df.info). Convert it to datetime first
        ecb_ts['TIME_PERIOD'] = pd.to_datetime(ecb_ts['TIME_PERIOD'])
        # Set 'TIME_PERIOD' to be the index
        ecb = ecb_ts.set_index('TIME_PERIOD')
        # Append individual dataframe to pd_list
        pd_list.append(ecb)
        #===============================================================
        
        # Now concatenate each individual yield curve dataframe from the list of dataframes,
        # collected in the loop, into one single dataframe
        df_final=pd.concat(pd_list, axis=1)
    return df_final