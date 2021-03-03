'''
Created on 27/08/2020

@author: MarkSchaafsma
'''

## Standard Libraries
import csv
from datetime import datetime
# JSON serialization for writing to file. Not for handling the JSON response. Rather, the 'requests' module handles responses to create JSON.
import json
import logging
import sys

## Local Source

## Module logger
logger = logging.getLogger(__name__)





def writeDictListToCsvFile(dictList, fileName, filePathAndName):
    '''
    Converts list of dictionary values to CSV
    '''

    try:
        
        # The following creates the fieldnames required by dictWriter.
        # However, it generates the fieldnames in a random order.
        # Definitely prefer to keep the column order as defined by the application, which has a logical structure. 
        #keys = set().union(*(d.keys() for d in dictList))   
        #print("set.union Keys")
        #for k in keys:
        #    print(k)

        # The following creates the fieldnames required by dictWriter.
        # This option creates it in the same as order as it was created by this application, which is preferred.
        # Assertion: We only get here if we have at least one item in the dictionary so we rely on distList[0] having data
        keys = tuple(dictList[0])
        #print("Enumerate Keys")
        #for k in keys:
        #    print(k)
        
        filePathAndName = filePathAndName + ".csv"

        # Data supplied by the API may contain unicode data not valid for SQL_Latin1_General_CP1_CI_AS collation being used by the Claims Reporting database.
        # Thus use the Python File Encoding and File Handling options to manage.
        # For more info, see:
        #    http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html    

        # File Encoding Options:
        #  - ascii              : Unicode code points in the range 0-0x7F (i.e. ASCII is a 7-bit encoding).
        #  - latin-1            : ASCII-compatible encoding that maps byte values directly to the first 256 Unicode code points.
        #                         Note that Windows has its own latin-1 variant called cp1252, but, unlike the ISO latin-1 implemented
        #                         by the Python codec with that name, the Windows specific variant doesn't map all 256 possible byte values.         
        
        # File Error Handling Options:
        #  - strict             : This is the default error handler that just raises "UnicodeDecodeError" for decoding problems and
        #                         "UnicodeEncodeError" for encoding problems.
        #  - surrogateescape    : Error handler Python uses for most OS facing APIs to gracefully cope with encoding problems in the data
        #                         supplied by the OS. It handles decoding errors by squirreling the data away in a little used part of the
        #                         Unicode code point space. When encoding, it translates those hidden away values back into the exact original
        #                         byte sequence that failed to decode correctly.
        #  - backslashreplace   : Error handler that converts code points that can't be represented in the target encoding to the equivalent
        #                         Python string numeric escape sequence.

        # The SQL Server Bulk Insert has been setup to expect "CRLF".
        # Thus use the Python NewLine options to manage.

        # New Line options:
        #  - Valid values of the stream include -  None, "", "\n", "\r", "\r\n"
        #  - Use newline='' as this produces the EOF marker "CRLF" which is required by the SQL Server Bulk Insert
        #  - The "CRLF" can be checked via Notepad++ > View > Show Symbol > Show End of Line    

        with open(filePathAndName, 'w', newline='', encoding="latin-1", errors="backslashreplace") as outputFile:
        #with open(filePathAndName, 'w', newline='', encoding="latin-1", errors="surrogateescape") as outputFile:
        #with open(filePathAndName, 'w', newline='', encoding="ascii", errors="surrogateescape") as outputFile:
        #with open(filePathAndName, 'w', newline='', encoding="ascii", errors="backslashreplace") as outputFile:
        #with open(filePathAndName, 'w', newline='') as outputFile:
        #with open(filePathAndName, 'w', newline='\n') as outputFile: 
            
            # DictWriter Signature
            #   DictWriter (
            #     filename,
            #     fieldnames,
            #     restval: str=str,
            #     extrasaction: str=str,
            #     dialect: str=str,
            #     *args,
            #     **kwds
            #   )
            
            dictWriter = csv.DictWriter(outputFile, keys, delimiter= '|')    # pipe character | 
            #dictWriter = csv.DictWriter(outputFile, keys)                   # uses default delimiter. i.e. ','
            dictWriter.writeheader()
            dictWriter.writerows(dictList)
    
        logger.info(f"{fileName:25} {'dictionary values saved to: ':33}{filePathAndName}")

    except:
        message = "ERROR writing " + fileName + " dictionary values to" 
        logger.error(f"{message:55}: {filePathAndName}")
        logger.error(f"{' ':55}: {sys.exc_info()[0]}")
        logger.error(f"{' ':55}: {sys.exc_info()[1]}")





def writeJsonDictToJsonFile(jsonDict):
    
    try:
        # Setup the filename
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        filename = "resources/json/bziclaims-" + str(timestamp) + ".json"
        
        # Open the file for writing and create it if it doesn't exist
        f = open(filename, "w+")
        
        # Serialize the JSON dictionary  
        jsonObject = json.dumps(jsonDict, indent = 4) 
    
        # Writing the file
        f.write(jsonObject)
    
        # close the file when done
        f.close()
        
        logger.info(f"{'JSON written to file':30}: /{filename}")

    except:
        logger.error(f"{'ERROR writing JSON to file'}")
        logger.error(f"{' ':55}: {sys.exc_info()[0]}")
        logger.error(f"{' ':55}: {sys.exc_info()[1]}")
        

        


def getPathDetails(thisConfig):
    
    # Get the path from config 
    path = thisConfig['SQL_BULKINSERT_INPUT_FILEPATH']

    # Determine if it is a standard windows file path or a UNC file path
    # i.e. A windows standard path contains black slashes and starts with a driver letter.
    #      A UNC path contains forward slashes and starts with forward slashes.

    # Then check if it finishes with the appropriate back or forward slashes.
    # If not, then add them.
    
    if path[0] == '/' and path [1] == '/':
        if path[-1] != '/' and path[-2] != '/':
            path = path + '//'       
    else:
        if path[-1] != "\\":
            path = path + "\\"

        
    return path    





def getCSVFileRowCount(filepath, suffix):
    
    try:
        # "filepath" supplied without the filename suffix. So append.
        # Suffix values expected: csv, txt.
        file = open(f"{filepath}.{suffix}")
        reader = csv.reader(file)
        rowCount = len(list(reader))
        
        # CSV files have a header row, so subtract 1 from the row count
        if suffix == 'csv':
            if rowCount > 0:
                rowCount -= 1
    except:
        rowCount = 0
                
     
    return rowCount
    
    
    
    
