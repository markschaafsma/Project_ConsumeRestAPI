'''
Purpose:

    This application calls the GetClaims API to retrieve claims data in JSON format and 
    then either insert new data or update existing data in the Claims Reporting database.
         
    The application can be run in two modes:
    
    1) API               - Call Get Claims API to retrieve data to be processed.
    2) CSV               - Read "csv" files to get data to be processed.

    With two run types:
         
    1) JSON              - Retrieves the JSON response only. It is not processed against the Claims Reporting database.
                           Use this in conjunction with keep-response: "true" to retrieve claims API data to a file. 
                           This may be for archive purposes, or possibly for forwarding to insurers, e.g.Youi.
    2) INSERT            - Bulk insert of retrieved data (for initial database loading).
                           The JSON response data is not checked against the DB data before insertion, although
                           unique constraints should prevent insertion of duplicate claims.

    More specific detail on run options can be ascertained from the pyConfig module or the README.md file.
         
Revision History:

    20/11/2020   Mark Schaafsma   Reorganise - Move logging setup from configure module to this module.
                                  This prevents duplicate file handler setup.
    29/07/2020   Mark Schaafsma   Created. 
         
'''

## Standard libraries
from datetime import datetime
import sys

## Local Libraries
import constant
import logging
import pyConfig
from control import fileProcessing, request
from database import insertControl
from models import job
from utilities import logUtils

## Create a module logger
#  __name__ not passed when this module at same level in the project heirarchy as the root logger.
logger = logging.getLogger()
#logger = logging.getLogger(__name__)





def main():
 
    # Initialization
    #------------------
    # Create a variable containing details about thisJob's configuration.
    thisConfig = pyConfig.genConfig()
    # Setup logging. 
    setupLogging(thisConfig)
    # Create a variable containing details about thisJob's execution.
    thisJob = job.setupJob()
    # Log/Display start time, environment and run configuration.
    logUtils.logJobStartDetails(thisConfig, thisJob)

    # Processing
    #--------------
    if thisConfig['APP_JOB_TYPE'].upper() == constant.API_JOB_TYPE:
        request.setupRequestAndCall(thisConfig, thisJob)

    if thisConfig['APP_JOB_TYPE'].upper() == constant.CSV_JOB_TYPE:
        fileProcessing.processCSVFiles(thisConfig, thisJob)

    # Finalization
    #----------------
    # If Foreign Key constraints in use, check tables are trusted or try to re-mark tables as trusted.  
    insertControl.remarkClaimTablesAsTrusted(thisConfig, thisJob)
    # Log/Display job finish summary.
    logUtils.logJobFinishDetails(thisConfig, thisJob)





def setupLogging(thisConfig):

    if thisConfig['LOG_LEVEL'].upper() == constant.LOG_LEVEL_DEBUG:
        loggingLevel = logging.DEBUG
    elif thisConfig['LOG_LEVEL'].upper() == constant.LOG_LEVEL_INFO:
        loggingLevel = logging.INFO
    elif thisConfig['LOG_LEVEL'].upper() == constant.LOG_LEVEL_WARNING:
        loggingLevel = logging.WARNING
    elif thisConfig['LOG_LEVEL'].upper() == constant.LOG_LEVEL_ERROR:
        loggingLevel = logging.ERROR
    elif thisConfig['LOG_LEVEL'].upper() == constant.LOG_LEVEL_CRITICAL:
        loggingLevel = logging.CRITICAL
    else:
        loggingLevel = logging.INFO

    ## Configure logging to the console.

    # Note, logging seems to require basicConfig to be defined first with one handler. Further handlers can be added later.
    logging.basicConfig(stream=sys.stdout, level=loggingLevel, format='%(asctime)s : %(levelname)-7s : %(filename)-20s%(lineno)-6d : %(message)s')
    #logging.basicConfig(stream=sys.stdout, level=loggingLevel, style='{', format="{asctime} : {levelname:7} : {filename:20}{lineno:6} : {message}")
    #logging.basicConfig(stream=sys.stdout, level=loggingLevel, format='%(asctime)s: %(levelname)s: %(name)s: %(message)s')

    ## Configure logging to a file handler

    if thisConfig['LOG_DIRECTORY'] != '':

        # Setup log filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        filename = f"{thisConfig['LOG_DIRECTORY']}logfile-{str(timestamp)}.log"

        # Create a file handler and set logging level.
        fileHandler = logging.FileHandler(filename)
        fileHandler.setLevel(loggingLevel)
            
        # Create a formatter and add to the handler
        formatter = logging.Formatter('%(asctime)s : %(levelname)-7s : %(filename)-20s%(lineno)-6d : %(message)s')
        fileHandler.setFormatter(formatter)
    
        # Add the handler to the logger
        logger.addHandler(fileHandler)
        #logging.root.addHandler(fileHandler)

        # Allow only one instance of file handler and stream handler
        #if len(logger.handlers) == 1:
            #logger.addHandler(fileHandler)
            #logger.addHandler(consoleHandler)





if __name__ == "__main__":
    main()

