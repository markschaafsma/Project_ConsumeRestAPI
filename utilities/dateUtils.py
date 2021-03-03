'''
Purpose:

    This module provides some datetime conversion functions.
         
Revision History:

    04/08/2020   Mark Schaafsma   Created 
         
'''


# Standard Libraries
from datetime import datetime
#from datetime import timezone
#from datetime import time

# Third Party Libraries
import pytz

# Local Source
import constant




def utcToLocal(utc_dt_iso, returnType=None):
#def utcToLocal(utc_dt_iso):
    
    # utc_dt is in ISO 8061 UTC format
    #  - ISO 8061 General Format:  YYYY-MM-DDThh:mm:ss[.nnnnnn][{+|-}hh:mm]
    #  - ISO 8061 UTC Format:      YYYY-MM-DDThh:mm:ss[.nnnnnn]Z                # i.e. Offseet == 00:00

    if (utc_dt_iso == None):
        return utc_dt_iso

    # Truncate the Z from the ISO 8061 UTC Format plus add UTC timezone to create a Python datetime aware object  
    utc_dt = datetime.fromisoformat(utc_dt_iso[0:23] + "+00:00")
 
    # Get local timezone and hence difference from utc
    # This could be more sophisticated to get timezone of loss location

#     for tz in pytz.all_timezones:
#         print(tz)
#     # Results
#     Australia/ACT
#     Australia/Adelaide
#     Australia/Brisbane
#     Australia/Broken_Hill
#     Australia/Canberra
#     Australia/Currie
#     Australia/Darwin
#     Australia/Eucla
#     Australia/Hobart
#     Australia/LHI
#     Australia/Lindeman
#     Australia/Lord_Howe
#     Australia/Melbourne
#     Australia/NSW
#     Australia/North
#     Australia/Perth
#     Australia/Queensland
#     Australia/South
#     Australia/Sydney
#     Australia/Tasmania
#     Australia/Victoria
#     Australia/West
#     Australia/Yancowinna

    local_dt= utc_dt.astimezone(pytz.timezone("Australia/Sydney"))

#     print(f"{'UTC time received from API:':35}{utc_dt_iso}")    
#     print(f"{'Converted to Python datetime:':35}{str(utc_dt):30}{'Timezone:':12}{str(utc_dt.tzinfo):24}{'Offset:':10}{utc_dt.utcoffset()}")       
#     print(f"{'Converted to local datetime:':35}{str(local_dt):30}{'Timezone:':12}{str(local_dt.tzinfo):24}{'Offset:':10}{local_dt.utcoffset()}")
#     print()   

    if returnType == constant.DT_AWARE_STRING:
        return str(local_dt)
    elif returnType == constant.DT_NAIVE_STRING:
        return str(local_dt)[0:18]
    elif returnType == constant.DT_AWARE_OBJECT:
        return local_dt
    elif returnType == constant.DT_NAIVE_OBJECT:
        return local_dt.replace(tzinfo=None)
    else:
        return local_dt.replace(tzinfo=None) 


    # Return datetime as a String including the offset e.g. '2018-10-17 10:00:00+11:00'
    # If using SQL Server Datetimeoffset columns, then need to pass datetime aware object as a string else DBMS drops offset. 
    #return str(local_dt)

    # Return datetime as a String excluding the offset e.g. '2018-10-17 10:00:00'
    # SQL Server Datetime columns passed as strings must exclude the offset component. 
    #return str(local_dt)[0:18]

    # Return datetime as a Python datetime aware object
    # When returning like this, MS SQL Server not storing the offset.  MS 11/08/2020    
    #return local_dt              

    #tz = pytz.timezone("Australia/Sydney")    
    #return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)



def naiveToAware(dt_naive):
    tz = pytz.timezone("Australia/Sydney") 
    dt_aware = tz.localize(dt_naive)
    return str(dt_aware)
    #return dt_aware
    # When returning like this, MS SQL Server not storing the offset.  MS 11/08/2020
    # See https://stackoverflow.com/questions/59529424/sql-server-datetimeoffset-changes-the-offset-of-a-tz-aware-datetime-to-the-syste
    # Main Points:
    #  - Run SQL Profiler to see just what is being sent to the server
    #  - What version of pyodbc is being used?
    #  - Is fast_executemany=True specified in the create_engine call?
    #  - Works with fast_executemany when sending the DateTime with an offset as a plain string instead of DateTime datatype.



