'''
Purpose:

    This module handles request processing.
         
Revision History:

    27/08/2020   Mark Schaafsma   Created. 
         
'''

## Standard Libraries
# URL request handling module. Not used. The requests module is used instead.
#import urllib.request 

## Third Party Libraries
# Apache2 HTTP library
import requests

## Local Libraries
from control import response
#from pyConfig import thisConfig
from utilities import logUtils





def setupRequestAndCall(thisConfig, thisJob):

    # Setup the API request
    # =====================

    # Setup the API URL
    url = thisConfig['API_URL']

    # Setup the API URL query parameters
    params = {
        'lastUpdated' : thisConfig['API_PARAM_LASTUPDATED']                
       ,'page' : thisConfig['API_PARAM_PAGE']
       ,'per_page' : thisConfig['API_PARAM_PERPAGE']
       ,'stream' : thisConfig['API_PARAM_STREAM']
    }    

    # Setup the API Header data
    requestHeaders = {
        'X-Auth-Token' : thisConfig['API_HEADER_AUTH_TOKEN']
       ,'Accept' : thisConfig['API_HEADER_ACCEPT']
    }

    # Log/Display the request data
    logUtils.logRequestDetails(url, params, requestHeaders)

    # Call the API
    claimsResponse = requests.get(url, headers=requestHeaders, params=params)
    
    # Log/Display the response data
    logUtils.logResponseData(claimsResponse, thisJob)
    #logUtils.logResponseData(claimsResponse)

    # Handle the response 
    if (claimsResponse.status_code == 200):
        response.processResponseHeader(claimsResponse, thisConfig, thisJob)
    else:
        # Log/Display the response status code
        logUtils.logResponseStatusCode(claimsResponse)

    return thisJob


