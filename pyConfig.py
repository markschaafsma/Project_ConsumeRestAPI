'''
Purpose:

    This module defines the job configuration and global variables used by the Claims Reporting application.


Configuration Options:

  INSURER                          Type: String; Default: ''
    Options:
     1) "ORG_1"                    - Process ORG_1 Claims.
     2) "ORG_2"                    - Process ORG_2 Claims.
     3) "ORG_3"                    - Process ORG_3 Claims.

  APP_JOB_TYPE                     Type: String; Default:. 'API'
    Options:
     1) "API"                      - Call Get Claims API to retrieve data to be processed.
     2) "CSV"                      - Read "csv" files to get data to be processed.

  APP_RUN_TYPE                     Type: String; Default: 'INSERT'
    Options:
     1) "JSON"                     - Retrieves the JSON response only. It is not processed against the Claims Reporting database.
                                     Use this in conjunction with keep-response: "true" to retrieve claims API data to a file.
     2) "INSERT"                   - Insert of retrieved data (for initial database loading).
                                     API data not checked against DB data before insertion (apart from duplicate constraints). 
                                     Perhaps option better labeled as: "simple" or "insert" or "insert-only".    
     3) "INSERT-AND-UPDATE"        - For reconciling and updating existing database.
                                     API data checked against database data, or perhaps against previously stored JSON,
                                     before insertion or update.
                                     Perhaps option better labeled as: "incremental" or "update" or "update-and-insert" or
                                     "full" or "complete". 

  APP_UPDATE_TYPE                  Type: String; Default: 'MANY'
    Options:
     1) "SINGLE"                   - This uses the T-SQL Insert and Update statements. It has the slowest performance
                                     but provides the best database error handling and integrity checking.
     2) "MANY"                     - This uses the T-SQL Insert and Update statements with the pyodbc option executemany.
                                     It's performance depends on whether the option fast_executemany is set to true or false.
                                     When true, performance is acceptably quick, processing in about a tenth of the time as SINGLE.
                                     When false, performance appears to be quicker than SINGLE, but not significantly so.
                                     The down side with executemany is that processing terminates if any DML error is encountered.
                                     Hence a lot of data validation has been built into the application to protect against this. 
     3) "BULK"                     - This uses the T-SQL Bulk Insert statement. It has the fastest performance but can not guarantee
                                     database integrity. Errors are logged to files requiring additional processes and procedures to
                                     ensure database integrity is maintained. The bulk insert takes input from a file which means SQL
                                     Server requires access to the file across the network. For ORG_1, at least across lower environments,
                                     the network SQL Server is hosted on can't see the network the application is hosted on.

  APP_KEEP_RESPONSE                Type: String; Default: 'FALSE'
    Options:
     1) "TRUE"                     - Write the JSON response from memory to file. 
     2) "FALSE"                    - Don't write the JSON response from memory to file. 


  API_URL                          Type: String; e.g. ""
   
  API_PARAM_LASTUPDATED            Type: String; Default: ""; e.g. "2018-01-01T14:00:00.000Z"
    Options:
     1) ""                         - All claims held by the system
     2) utc date/time              - All claims since LastUpdated date in UTC Format e.g. "YYYY-MM-DDThh:mm:ss.mmmZ"
   
  API_PARAM_PAGE                   Type: Integer; Default: 1
   
  API_PARAM_PERPAGE                Type: Integer; Default: 5000
  
  API_PARAM_STREAM                 Type: Boolean; Default: False
    Options:
     1) True                       - Retrieve data in stream mode - all data meeting the LastUpdate criteria retrieved in one call - but maybe inefficient.
     2) False                      - Retrieve data in pagination mode - only data up to the specified page limit retrieved per call - maybe more efficient.


  SQL_BULKINSERT_INPUT_FILEPATH    Type: String; Default "";
                                   e.g. '\\\\DESKTOP-XXXXXXX\\ClaimsReporting\\temp\\csvfiles\\'
                                     or 'C:\\ProgramData\\ClaimsReporting\\temp\\csvfiles\\'
    Notes:
     1) This is the location where bulk insert data files will be written to and read from.
     2) The file location MUST exist, else the file write will fail!!!
     3) The file location must be the full path.
     4) If data_file is a local file to the server, then the data_file must specify a valid path from the server on which SQL Server is running.
        e.g. "C:\\ProgramData\\ClaimsReporting\\temp\\csvfiles\\"
     6) The path MUST use double \\, that is, a \ to escape the \

     5) If data_file is a remote file, specify the Universal Naming Convention (UNC) name.    
        i.e. \\Systemname\ShareName\Path\FileName
        e.g. \\\\DESKTOP-XXXXXXX\\ClaimsReporting\\temp\\csvfiles\\
             \\\\AZURE-USQL\\ClaimsReporting\\temp\\csvfiles\\        

     7) The path requires the \\ at the end, although the application will check for it and add if necessary.
     
     8) Full details: https://docs.microsoft.com/en-us/sql/t-sql/statements/bulk-insert-transact-sql?redirectedfrom=MSDN&view=sql-server-ver15
      
  SQL_BULKINSERT_BATCHSIZE         Type: Integer; Default: 1000 
    Notes:
     1) This is the number of records processed in a batch and committed at one time.
     2) With this option though, if one batch fails all batches are rolled back.
     2) Datatype is integer - that is, enter without quotes.

  SQL_BULKINSERT_MAXERRORS         Type: Integer; Default: 5000
    Notes:
     1) Job will terminate if the maximum number of errors is reached.
     2) Datatype is integer - that is, enter without quotes.

  LOG_LEVEL                        Type: String; Default: "INFO"
    Options:
     1) "DEBUG"                    - Detailed information, typically of interest only when diagnosing problems.
     2) "INFO"                     - Confirmation that things are working as expected.
     3) "WARNING"                  - An indication that something unexpected happened. The software is still working as expected.
     4) "ERROR"                    - Due to a more serious problem, the software has not been able to perform some function.
     5) "CRITICAL"                 - A serious error, indicating that the program itself may be unable to continue running.

  LOG_DIRECTORY                    Type: String; Default ''
                                   e.g. '\\\\DESKTOP-XXXXXXX\\ClaimsReporting\\dev\\logs\\'
                                     or 'C:\\ProgramData\\ClaimsReporting\\dev\\logs\\'
    Notes:
     1) This is the location where log files will be written to.
         
Revision History:

    16/11/2020   Mark Schaafsma   Added logging parameters and validation.
    12/10/2020   Mark Schaafsma   Added further parameter validation and default processing.
    14/09/2020   Mark Schaafsma   Added APP_JOB_TYPE parameter.
    18/08/2020   Mark Schaafsma   Created. 
         
'''

## Standard Libraries
import os
                              
## Local Libraries
import constant




   
def genConfig():

    config = dict()

    try:
        config['ENV'] = os.environ['ENV']
    except:
        config['ENV'] = constant.LOC_ENV
    
    try:
        config['INSURER'] = os.environ['insurer']
    except:
        config['INSURER'] = constant.ZURICH

    
    if str(config['ENV']).upper() == constant.UAT_ENV:

        # Application Parameters
        config['APP_JOB_TYPE'] = 'api'
        config['APP_RUN_TYPE'] = 'insert'
        config['APP_UPDATE_TYPE'] = 'many'
        config['APP_UPDATE_TYPE_FAST_EXECUTEMANY'] = True
        config['APP_KEEP_RESPONSE'] = 'false'
        config['APP_RESPONSE_DIRECTORY'] = ''

        # API Parameters        
        config['API_URL'] = ''
        config['API_PARAM_LASTUPDATED'] = ''
        config['API_PARAM_PAGE'] = 1
        config['API_PARAM_PERPAGE'] = 5000
        config['API_PARAM_STREAM'] = False
        
        if config['INSURER'].upper() == constant.ORG_1:  
            config['API_HEADER_AUTH_TOKEN'] = ''
        elif config['INSURER'].upper() == constant.ORG_2:
            config['API_HEADER_AUTH_TOKEN'] = ''
        elif config['INSURER'].upper() == constant.ORG_3:
            config['API_HEADER_AUTH_TOKEN'] = ''
        else:
            config['API_HEADER_AUTH_TOKEN'] = ''
        
        config['API_HEADER_ACCEPT'] = 'application/json'

        # SQL Server Database Parameters        
        config['SQL_DATABASE_IP'] = '###'
        config['SQL_DATABASE_NAME'] = '###'
        config['SQL_DATABASE_USERNAME'] = '###'
        config['SQL_DATABASE_PASSWORD'] = '###'        
        
        # For remote, specify in UNC format as follows where:
        #   '\\\\ShareName' refers to a Share drive that has been established.        
        config['SQL_BULKINSERT_INPUT_FILEPATH'] = '\\\\ShareName\\uat\\csvfiles\\'
        config['SQL_BULKINSERT_BATCHSIZE'] = 5000
        config['SQL_BULKINSERT_MAXERRORS'] = 10000
        
        config['LOG_LEVEL'] = 'INFO'
        config['LOG_DIRECTORY'] = 'C:\\ClaimsReporting\\uat\\logs\\'

    
    elif (str(config['ENV']).upper() == constant.LOC_ENV
       or str(config['ENV']).upper() == constant.DEV_ENV):

        # Application Parameters
        config['APP_JOB_TYPE'] = 'api'
        config['APP_RUN_TYPE'] = 'insert'
        config['APP_UPDATE_TYPE'] = 'many'
        config['APP_UPDATE_TYPE_FAST_EXECUTEMANY'] = True
        config['APP_KEEP_RESPONSE'] = 'false'
        config['APP_RESPONSE_DIRECTORY'] = ''

        # API Parameters      
        config['API_URL'] = ''
        config['API_PARAM_LASTUPDATED'] = ''
        #config['API_PARAM_LASTUPDATED'] = '2018-01-01T14:00:00.000Z'
        config['API_PARAM_PAGE'] = 1
        config['API_PARAM_PERPAGE'] = 5000
        config['API_PARAM_STREAM'] = False
    
        if config['INSURER'].upper() == constant.ORG_1:  
            config['API_HEADER_AUTH_TOKEN'] = ''
        elif config['INSURER'].upper() == constant.ORG_2:
            config['API_HEADER_AUTH_TOKEN'] = ''
        elif config['INSURER'].upper() == constant.ORG_3:
            config['API_HEADER_AUTH_TOKEN'] = ''
        else:
            config['API_HEADER_AUTH_TOKEN'] = ''
        
        config['API_HEADER_ACCEPT'] = 'application/json'

        # SQL Server Database Parameters              
        config['SQL_DATABASE_IP'] = ''
        config['SQL_DATABASE_NAME'] = 'DEV_CLAIMS'
        config['SQL_DATABASE_USERNAME'] = ''
        config['SQL_DATABASE_PASSWORD'] = ''        


        # For remote, specify in UNC format as follows:
        config['SQL_BULKINSERT_INPUT_FILEPATH'] = '\\\\DESKTOP-XXXXXX\\ClaimsReporting\\dev\\csvfiles'        
        # For remote, forward slashes also works as follows:
        #config['SQL_BULKINSERT_INPUT_FILEPATH'] = '//DESKTOP-XXXXXXX//ClaimsReporting//dev//csvfiles//'
        # For local specify as follows:
        #config['SQL_BULKINSERT_INPUT_FILEPATH'] = 'C:\\ProgramData\\ClaimsReporting\\dev\\csvfiles\\'
        config['SQL_BULKINSERT_BATCHSIZE'] = 5000
        config['SQL_BULKINSERT_MAXERRORS'] = 5000
        
        config['LOG_LEVEL'] = 'INFO'
        config['LOG_DIRECTORY'] = 'C:\\ProgramData\\ClaimsReporting\\dev\\logs\\'




    # The following section provides some validation of the configuration parameters provided.
    # For example:
    #  - Data type for each configuration item is correct. i.e. character, integer, boolean.
    #  - Value is a valid value. e.g. API_PARAM_STREAM is either True or False.
    #
    # Depending on the parameter, either display a message and terminate, or set a default.

    if not isinstance(config['APP_JOB_TYPE'], str):
        print(f"{'Invalid job parameter supplied':30}: APP-JOB-TYPE: {config['APP-JOB-TYPE']}")
        print(f"{'Valid values are:':30}: 'API' or 'CSV'")
        print(f"Job terminated.")
        quit()
    else:    
        if not (config['APP_JOB_TYPE'].upper() == constant.API_JOB_TYPE
             or config['APP_JOB_TYPE'].upper() == constant.CSV_JOB_TYPE):
            # If no value supplied, default to API_JOB_TYPE, else terminate.
            if config['APP_JOB_TYPE'].upper() == '':
                config['APP_JOB_TYPE'] = constant.API_JOB_TYPE
            else:
                print(f"{'Invalid job parameter supplied':30}: APP-JOB-TYPE: {config['APP-JOB-TYPE']}")
                print(f"{'Valid values are:':30}: {constant.API_JOB_TYPE} or {constant.CSV_JOB_TYPE}")
                print(f"Job terminated.")
                quit()


    if not isinstance(config['APP_RUN_TYPE'], str):
        print(f"{'Invalid job parameter supplied':30}: APP-RUN-TYPE: {config['APP_RUN_TYPE']}")
        print(f"{'Valid values are':30}: 'JSON', 'INSERT' or 'INSERT-AND-UPDATE'")
        print(f"Job terminated.")
        quit()
    else:          
        if not (config['APP_RUN_TYPE'].upper() == constant.JSON_RUN_TYPE
             or config['APP_RUN_TYPE'].upper() == constant.INSERT_RUN_TYPE
             or config['APP_RUN_TYPE'].upper() == constant.INSERT_AND_UPDATE_RUN_TYPE):
            # If no value supplied, default to INSERT_RUN_TYPE, else terminate.
            if config['APP_RUN_TYPE'].upper() == '':
                config['APP_RUN_TYPE'] = constant.INSERT_RUN_TYPE
            else:
                print(f"{'Invalid job parameter supplied':30}: APP-RUN-TYPE: {config['APP_RUN_TYPE']}")
                print(f"{'Valid values are':30}: {constant.JSON_RUN_TYPE}, {constant.INSERT_RUN_TYPE} or {constant.INSERT_AND_UPDATE_RUN_TYPE}")
                print(f"Job terminated.")
                quit()
        if (config['APP_RUN_TYPE'].upper() == constant.INSERT_AND_UPDATE_RUN_TYPE):
            print(f"{'This option not yet implemented.':30}: APP-RUN-TYPE: {config['APP_RUN_TYPE']}")
            print(f"Job terminated.")
            quit()


    if not isinstance(config['APP_UPDATE_TYPE'], str):
        print(f"{'Invalid job parameter supplied':30}: APP_UPDATE_TYPE: {config['APP_UPDATE_TYPE']}")
        print(f"{'Valid values are':30}: {constant.SINGLE_UPDATE_TYPE}, {constant.MANY_UPDATE_TYPE} or {constant.BULK_UPDATE_TYPE}")
        quit()
    else:
        if not (config['APP_UPDATE_TYPE'].upper() == constant.SINGLE_UPDATE_TYPE
             or config['APP_UPDATE_TYPE'].upper() == constant.MANY_UPDATE_TYPE
             or config['APP_UPDATE_TYPE'].upper() == constant.BULK_UPDATE_TYPE):
            # If no value supplied, default to BULK_UPDATE_TYPE, else terminate.
            if config['APP_UPDATE_TYPE'].upper() == '':
                config['APP_UPDATE_TYPE'] = constant.BULK_UPDATE_TYPE
            else:
                print(f"{'Invalid job parameter supplied':30}: APP_UPDATE_TYPE: {config['APP_UPDATE_TYPE']}")
                print(f"{'Valid values are':30}: {constant.SINGLE_UPDATE_TYPE}, {constant.MANY_UPDATE_TYPE} or {constant.BULK_UPDATE_TYPE}")
                quit()


    if not isinstance(config['APP_UPDATE_TYPE_FAST_EXECUTEMANY'], bool):
        # If no value supplied, or invalid datatype supplied, default to False.
        config['APP_UPDATE_TYPE_FAST_EXECUTEMANY'] = True


    if not isinstance(config['APP_KEEP_RESPONSE'], str):
        config['APP_KEEP_RESPONSE'] = constant.FALSE_KEEP_RESPONSE
    else:
        # If no value supplied, default to FALSE_KEEP_RESPONSE.
        if not (config['APP_KEEP_RESPONSE'].upper() == constant.TRUE_KEEP_RESPONSE
             or config['APP_KEEP_RESPONSE'].upper() == constant.FALSE_KEEP_RESPONSE):
            config['APP_KEEP_RESPONSE'] = constant.FALSE_KEEP_RESPONSE


    if not isinstance(config['APP_RESPONSE_DIRECTORY'], str):
        if config['APP_KEEP_RESPONSE'].upper() == constant.FALSE_KEEP_RESPONSE:
            config['APP_RESPONSE_DIRECTORY'] = ''
        else:
            print(f"{'Invalid job parameter supplied':30}: APP_RESPONSE_DIRECTORY: {config['APP_RESPONSE_DIRECTORY']}")
            print(f"{'Value should be passed as a string in quote marks'}")
            print(f"Job terminated.")
            quit()


    if not isinstance(config['API_URL'], str):
        print(f"{'Invalid job parameter supplied':30}: API_URL: {config['API_URL']}")
        print(f"{'Value should be passed as a string in quote marks'}")
        quit()


    if not isinstance(config['API_PARAM_LASTUPDATED'], str):
        print(f"{'Invalid job parameter supplied':30}: API_PARAM_LASTUPDATED: {config['API_PARAM_LASTUPDATED']}")
        print(f"{'Value should be passed as a string in UTC date format: YYYY-MM-DDThh:mm:ss.mmmZ'}")
        config['API_PARAM_LASTUPDATED'] = ''

    if not isinstance(config['API_PARAM_PAGE'], int):
        config['API_PARAM_PAGE'] = 1

    if not isinstance(config['API_PARAM_PERPAGE'], int):
        config['API_PARAM_PERPAGE'] = 5000

    if not isinstance(config['API_PARAM_STREAM'], bool):
        config['API_PARAM_STREAM'] = False


    if not isinstance(config['SQL_BULKINSERT_INPUT_FILEPATH'], str):
        print(f"{'Invalid job parameter supplied':30}: SQL_BULKINSERT_INPUT_FILEPATH: {config['SQL_BULKINSERT_INPUT_FILEPATH']}")
        print(f"{'Value should be passed as a string in quote marks':30}")
        quit()

    if not isinstance(config['SQL_BULKINSERT_BATCHSIZE'], int):       
        config['SQL_BULKINSERT_BATCHSIZE'] = 5000

    if not isinstance(config['SQL_BULKINSERT_MAXERRORS'], int):       
        config['SQL_BULKINSERT_MAXERRORS'] = 5000


    if not isinstance(config['LOG_LEVEL'], str):
        print(f"{'Invalid job parameter supplied':30}: LOG_LEVEL: {config['LOG_LEVEL']}")
        print(f"{'Valid values are:':30}: {constant.LOG_LEVEL_DEBUG}, {constant.LOG_LEVEL_INFO}, {constant.LOG_LEVEL_WARNING}, {constant.LOG_LEVEL_ERROR} or {constant.LOG_LEVEL_CRITICAL}")
        print(f"Job terminated.")
        quit()

    if not isinstance(config['LOG_DIRECTORY'], str):
        print(f"{'Invalid job parameter supplied':30}: LOG_DIRECTORY: {config['LOG_DIRECTORY']}")
        print(f"{'Value should be passed as a string in quote marks'}")
        print(f"Job terminated.")
        quit()

    
    return config



