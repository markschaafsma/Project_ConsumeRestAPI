'''
Purpose:

    This module handles response processing.
         
Revision History:

    27/08/2020   Mark Schaafsma   Created.
         
'''

## Standard Libraries
import logging
import re

## Local Libraries
import constant
from control import hash
from database import selectControl, insertControl, updateControl, execute 
from models import mappings
from utilities import fileUtils, logUtils

## Create a module logger
logger = logging.getLogger(__name__)





def processResponseHeader(response, thisConfig, thisJob):
    
    # Convert the response into JSON
    # JSON contents can then be accessed like any other Python object/dictionary.
    theJSON = response.json()

    # Log/Display response data summary
    logUtils.logResponseSummary(theJSON, thisConfig, thisJob)
 
    # Write the JSON response from memory to a file or log any exceptions.
    logUtils.logKeepResponse(theJSON, thisConfig)
    
    # Log/Display Run Type
    logUtils.logRunTypeDetails(thisConfig)

    # Determine database processing required
    if str(thisConfig['APP_RUN_TYPE']).upper() == constant.INSERT_RUN_TYPE:
        processResponseDetail(theJSON, thisConfig, thisJob)

    elif str(thisConfig['APP_RUN_TYPE']).upper() == constant.INSERT_AND_UPDATE_RUN_TYPE:
        # TODO: Setup this processing.
        pass
        #processResponseDetail(theJSON)





def processResponseDetail(theJSON, thisConfig, thisJob):

    # Log/Display processing log start
    logUtils.logProcessingLogHeader()
    
    # Get the list of Claims to be processed
    if 'items' in theJSON.get('master_reports'):
        
        claims = theJSON.get('master_reports').get('items')

        # For BULK claim insert processing, the application will manage the allocation of the Primary Keys.
        # For SINGLE claim insert processing, the DBMS will can manage the allocation of the Primary Keys.
        #
        # Note though:
        #  - The application will include Primary Keys in the table dictionaries it prepares irrespective
        #    of whether the processing mode is SINGLE or BULK.
        #  - Likewise, the application will manage the allocation of Foreign Keys in the table dictionaries.   
        #  - If processing is SINGLE, the DMBS will ignore the Primary Key supplied in the dictionaries.
        #
        # Also note:
        #  - Application management of Primary and Foreign Keys requires some level of concurrency control
        #    to guarantee no table inserts outside of this this batch process occur during this batch process.
        
        

        # Define table dictionary lists.
        #           
        # Note:
        #   These dictionaries need to be accessed from different functions and modules through out the application.
        #   So they need to be combined into an overall claims list or claims object in some fashion.
             
        ClaimObjectList = list()
        ClaimHeaderList = list()
        ClaimInsuredList = list()
        ClaimBrokerList = list()
        ClaimStatusHistoryList = list()
        ClaimFeedbackList = list()
        ClaimMotorDetailList = list()
        ClaimReserveMovementList = list()
        ClaimPaymentList = list()
        ClaimPaymentDetailList = list()
        ClaimPaymentHistoryList = list()
        ClaimRecoveryList = list()
        ClaimRecoveryDetailList = list()
        ClaimRecoveryHistoryList = list()

        # Setup an overall Claims List to facilitate passing the data around the application 
        ClaimsList = list()
        ClaimsList.append(ClaimObjectList)
        ClaimsList.append(ClaimHeaderList)
        ClaimsList.append(ClaimInsuredList)
        ClaimsList.append(ClaimBrokerList)
        ClaimsList.append(ClaimStatusHistoryList)
        ClaimsList.append(ClaimMotorDetailList)
        ClaimsList.append(ClaimFeedbackList)
        ClaimsList.append(ClaimReserveMovementList)
        ClaimsList.append(ClaimPaymentList)
        ClaimsList.append(ClaimPaymentDetailList)
        ClaimsList.append(ClaimPaymentHistoryList)
        ClaimsList.append(ClaimRecoveryList)
        ClaimsList.append(ClaimRecoveryDetailList)
        ClaimsList.append(ClaimRecoveryHistoryList)


           
        # To initiate management of Primary and Foreign Keys, get the last identity value
        # (Primary Key) inserted into each table and increment it by the table Identity Increment.
        # We know for this database all tables are using an Identity Increment of 1 and this is
        # unlikely to change.
        identityIncrement = 1
        
        # Log/Display Current Identities processing start.
        logUtils.logCurrentIdentityHeader()

        # Set the primary key to be used for each table.
        claimId = int(selectControl.getCurrentIdentity('ClaimHeader', thisConfig) + identityIncrement)
        claimInsuredId = int(selectControl.getCurrentIdentity('ClaimInsured', thisConfig) + identityIncrement)
        claimBrokerId = int(selectControl.getCurrentIdentity('ClaimBroker', thisConfig) + identityIncrement)
        claimStatusHistoryId = int(selectControl.getCurrentIdentity('ClaimStatusHistory', thisConfig) + identityIncrement)
        claimFeedbackId = int(selectControl.getCurrentIdentity('ClaimFeedback', thisConfig) + identityIncrement)
        claimMotorDetailId = int(selectControl.getCurrentIdentity('ClaimMotorDetail', thisConfig) + identityIncrement)
        claimReserveMovementId = int(selectControl.getCurrentIdentity('ClaimReserveMovement', thisConfig) + identityIncrement)
        claimPaymentId = int(selectControl.getCurrentIdentity('ClaimPayment', thisConfig) + identityIncrement)
        claimPaymentDetailId = int(selectControl.getCurrentIdentity('ClaimPaymentDetail', thisConfig) + identityIncrement)
        claimPaymentHistoryId = int(selectControl.getCurrentIdentity('ClaimPaymentHistory', thisConfig) + identityIncrement)
        claimRecoveryId = int(selectControl.getCurrentIdentity('ClaimRecovery', thisConfig) + identityIncrement)
        claimRecoveryDetailId = int(selectControl.getCurrentIdentity('ClaimRecoveryDetail', thisConfig) + identityIncrement)
        claimRecoveryHistoryId = int(selectControl.getCurrentIdentity('ClaimRecoveryHistory', thisConfig) + identityIncrement)

        # Log/Display Data Validation and Mapping processing start.
        logUtils.logDataValidationHeader()

        # For each database table, load data into a corresponding dictionary.
        # Then depending on whether SINGLE or BULK processing, save the dictionary in a list,
        # or use the dictionary values to immediately insert a table row.
        # ======================================================================================

        for claim in claims:

            # Setup a dictionary to store hash values for each dictionary in the claim. 
            ClaimObjectHashDict = dict()

            # ClaimHeader processing
            # ----------------------
            # processing removed



            # ClaimInsured processing
            # -----------------------
            # processing removed



            # ClaimBroker processing
            # ----------------------
            # processing removed



            # ClaimStatusHistory processing
            # -----------------------------
            # processing removed



            # ClaimMotorDetail processing
            # ---------------------------
            # processing removed



            # ClaimFeedback processing
            # ------------------------
            # processing removed



            # ClaimReserveMovement processing
            # -------------------------------
            # processing removed



            # ClaimPayment processing
            # -----------------------
            # processing removed


                    # ClaimPaymentDetail processing
                    # -----------------------------                    
                    # processing removed



                    # ClaimPaymentHistory processing
                    # ------------------------------
                    # processing removed



            # ClaimRecovery processing
            #-------------------------
            # processing removed


                    # ClaimRecoveryDetail processing
                    # ------------------------------
                    # processing removed



                    # ClaimRecoveryHistory processing
                    # -------------------------------
            # processing removed



            # Claim key management processing
            #--------------------------------
            # processing removed




        # --- End of claim in claims for loop --- #      


        # Write Table Dictionary Lists to the file system.
        # For Bulk Insert, this is required before database processing.
        processTableDictListsWritingToFile(ClaimsList, thisConfig)                


        # From this point the application starts working with the database.
        # For simplicity, and to maximize the likelihood of successfully updating the database,
        # pessimistic concurrency control could be used.
        #
        # The following table presents the isolation level options available:
        #
        #   Isolation level      Dirty read    Non-Repeatable read    Phantom
        #   Read uncommitted        Yes             Yes                 Yes
        #   Read committed          No              Yes                 Yes
        #   Repeatable read         No              No                  Yes
        #   Snapshot                No              No                  No
        #   Serializable            No              No                  No
        # 
        # When the isolation level is specified, the locking behavior for all queries and data manipulation language (DML)
        # statements in the SQL Server session operates at that isolation level. The isolation level remains in effect until
        # the session terminates or until the isolation level is set to another level.
        #
        # Isolation level Serializable provides the most pessimistic concurrency and is the intended level to be used.
        #
        # For more info see: https://docs.microsoft.com/en-us/sql/relational-databases/sql-server-transaction-locking-and-row-versioning-guide
        #
        # Note: This comment is currently located within the response.py module, but applies to the filePprocessing.py module too.
        #       So if implemented, needs to be setup elsewhere, execute.py perhaps, and called from each module as appropriate.    
        #
        #
        #    SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;  
        #    GO  
        #    BEGIN TRANSACTION; 
        #
        #        -- processing --
        #

        # Perform Insert processing
        processTableDictListsPerformingInserts(ClaimsList, thisConfig, thisJob)

        # Perform Update processing
        processTableDictListsPerformingUpdates(ClaimHeaderSetToNotCurrentList, thisConfig, thisJob)

        #
        #    END TRANSACTION;
        #


    else:
        logger.info(f"The claims JSON document does not contain any 'items' within 'master_reports'")





def processTableDictListsWritingToFile(ClaimsList, thisConfig):

    # Write each table dictionary list to a data "csv" file

    # Log/Display csv file processing start
    logUtils.logCsvFileHeader()

    path = fileUtils.getPathDetails(thisConfig)

    # Data "csv" files will overwrite previous files in the same location.
    # However, this job will fail if previous error files (from Bulk Insert processing) still exist.
    #   e.g. ClaimHeader.txt            -  Contains rejected/unprocessed data
    #        ClaimHeader.txt.Error.Txt  -  Contains brief error messages

    # If dictionary contains zero items, no file will be written.
    # Note: If no file is written for a dictionary, then the previous file will still exist on the file system.
    #       So double check create dates when using the files.
    
    for ClaimsTableDictList in ClaimsList:
            
        if len(ClaimsTableDictList) > 0:
            
            table = determineTableBeingProcessed(ClaimsTableDictList)
                
            # Append table name to path but don't add file suffix.
            # Suffixes "csv" and "err" will be added later by the SQL preparation processing.
            pathWithFileName = f"{path}{table}"

            # Translate Python boolean (True/False) values to SQL Server bit (1/0) values required by the Bulk Insert.
            translatedClaimsTableDictList = translateFieldsForBulkInsertFileFormat(table, ClaimsTableDictList)

            # Write the table dictionary to a data (csv) file (in the format required by SQL Server Bulk Insert).
            # This format is also works with 'CSV'/'Single' record processing, but not 'CSV'/'Many' record processing.
            # For 'CSV'/'Many' processing, the csv file will need to be transalted to the required format.  
            fileUtils.writeDictListToCsvFile(translatedClaimsTableDictList, table, pathWithFileName)

            # Alternatively, can write in different formats depending on the type of processing being run.
            # Probably simpler to write in one format and handle that format depending on the type of processing
            # requested when feeding the csv files back in.
            # So the following code is commented out. 

            # if thisConfig['APP_UPDATE_TYPE'].upper() == constant.MANY_UPDATE_TYPE:
            #     # Write the table dictionary to a data (csv) file (in the format required by pyodbc.executemany).
            #     fileUtils.writeDictListToCsvFile(ClaimsTableDictList, table, pathWithFileName)
            # else:
            #     # Translate Python boolean (True/False) values to SQL Server bit (1/0) values required by the Bulk Insert.
            #     translatedClaimsTableDictList = translateFieldsForBulkInsertFileFormat(table, ClaimsTableDictList)
            #     # Write the table dictionary to a data (csv) file (in the format required by SQL Server Bulk Insert).
            #     fileUtils.writeDictListToCsvFile(translatedClaimsTableDictList, table, pathWithFileName)





def processTableDictListsPerformingInserts(ClaimsList, thisConfig, thisJob):

    logUtils.logInsertProcessingHeader()

    # Create a tableList while processing the ClaimsTableDictList
    tableList = list()

    path = fileUtils.getPathDetails(thisConfig)

    for ClaimsTableDictList in ClaimsList:
            
        if len(ClaimsTableDictList) > 0:
            
            table = determineTableBeingProcessed(ClaimsTableDictList)
            tableList.append(table)

            if thisConfig['APP_UPDATE_TYPE'].upper() == constant.BULK_UPDATE_TYPE:

                # Append table name to path but don't add file suffix.
                # Suffixes "csv" and "err" will be added later by the SQL preparation processing.
                filepath = f"{path}{table}"
                
                # Now run the bulk inserts using the file as input.
                insertControl.insertBulkClaimTableRows(table, filepath, thisConfig, thisJob)


            if thisConfig['APP_UPDATE_TYPE'].upper() == constant.MANY_UPDATE_TYPE:

                # Run fast_executemany inserts using the dictionaries as input.
                insertControl.insertManyClaimTableRows(table, ClaimsTableDictList, thisConfig, thisJob)


            if thisConfig['APP_UPDATE_TYPE'].upper() == constant.SINGLE_UPDATE_TYPE:

                # Run standard inserts using the dictionaries as input.
                insertControl.insertClaimTableRow(table, ClaimsTableDictList, thisConfig, thisJob)


        


def determineTableBeingProcessed(ClaimsTableDictList):

    # Ascertain which TableDictionaryList is being processed by checking the PK field name key, and a few other field name keys.
    table = ''

    if ('ClaimId' in ClaimsTableDictList[0]
    and 'ClaimHash' in ClaimsTableDictList[0]):
        table = "ClaimObject"

    if ('ClaimId' in ClaimsTableDictList[0]
    and 'ClaimNo' in ClaimsTableDictList[0]):
        table = "ClaimHeader"
        
    elif ('ClaimInsuredId' in ClaimsTableDictList[0]
      and 'InsuredName'    in ClaimsTableDictList[0]):
        table = "ClaimInsured"
        
    elif ('ClaimBrokerId' in ClaimsTableDictList[0]
      and 'HeadOffice'    in ClaimsTableDictList[0]):
        table = "ClaimBroker"
        
    elif ('ClaimStatusHistoryId' in ClaimsTableDictList[0]
      and 'StatusCreated'        in ClaimsTableDictList[0]):
        table = "ClaimStatusHistory"

    elif ('ClaimFeedbackId' in ClaimsTableDictList[0]
      and 'DateGiven'       in ClaimsTableDictList[0]):
        table = "ClaimFeedback"

    elif ('ClaimMotorDetailId' in ClaimsTableDictList[0]
      and 'VehicleMake'        in ClaimsTableDictList[0]):
        table = "ClaimMotorDetail"

    elif ('ClaimReserveMovementId' in ClaimsTableDictList[0]
      and 'MovementNo'             in ClaimsTableDictList[0]):
        table = "ClaimReserveMovement"

    elif ('ClaimPaymentId' in ClaimsTableDictList[0]
      and 'PaymentNo'      in ClaimsTableDictList[0]):
        table = "ClaimPayment"

    elif ('ClaimPaymentDetailId' in ClaimsTableDictList[0]
      and 'PaymentDetailNo'      in ClaimsTableDictList[0]):
        table = "ClaimPaymentDetail"

    elif ('ClaimPaymentHistoryId' in ClaimsTableDictList[0]
      and 'StatusCreated'         in ClaimsTableDictList[0]):
        table = "ClaimPaymentHistory"

    elif ('ClaimRecoveryId' in ClaimsTableDictList[0]
      and 'RecoveryNo'      in ClaimsTableDictList[0]):
        table = "ClaimRecovery"

    elif ('ClaimRecoveryDetailId' in ClaimsTableDictList[0]
      and 'RecoveryDetailNo'      in ClaimsTableDictList[0]):
        table = "ClaimRecoveryDetail"

    elif ('ClaimRecoveryHistoryId' in ClaimsTableDictList[0]
      and 'StatusCreated'          in ClaimsTableDictList[0]):
        table = "ClaimRecoveryHistory"
    

    return table





def processTableDictListsPerformingUpdates(ClaimHeaderSetToNotCurrentList, thisConfig, thisJob):

    logUtils.logUpdateProcessingHeader()

    # Perform set ClaimHeaderRowsNotCurrent update processing.
    for tableDetail in thisJob['TableDetails']:
        if tableDetail['ClaimTable'] == 'ClaimHeader':
            if tableDetail['FailedInserts'] == 0:
                processClaimHeaderSetToNotCurrentUpdates(ClaimHeaderSetToNotCurrentList, thisConfig, thisJob)
            else:
                logger.warning(f"Set ClaimHeaderRowsNotCurrent update processing not run since ClaimHeader insert processing failed. ClaimHeader.IsCurrentVersion maybe inconsistent now.")





def processClaimHeaderSetToNotCurrentUpdates(ClaimHeaderSetToNotCurrentList, thisConfig, thisJob):

    # Currently only one method available to do updates; a single row at a time. 

    updateControl.updateSingleClaimHeaderCurrentVersionRows(ClaimHeaderSetToNotCurrentList, thisConfig, thisJob)
    #updateControl.updateSingleClaimHeaderCurrentVersionRows(ClaimHeaderSetToNotCurrentList, thisConfig, thisJob)


    # if thisConfig['APP_UPDATE_TYPE'].upper() == constant.MANY_UPDATE_TYPE:

    #     # Run fast_executemany updates using the dictionaries as input.
    #     updateControl.updateManyClaimHeaderCurrentVersionRows(ClaimHeaderSetToNotCurrentList, thisConfig, thisJob)


    # if thisConfig['APP_UPDATE_TYPE'].upper() == constant.SINGLE_UPDATE_TYPE:

    #     # Run standard updates using the dictionaries as input.
    #     updateControl.updateSingleClaimHeaderCurrentVersionRows(ClaimHeaderSetToNotCurrentList, thisConfig, thisJob)





def translateFieldsForBulkInsertFileFormat(table, dictList):

    # CSV format required by Bulk Insert is different to that required by Pyodbc.ExecuteMany.
    # This creates the format required by Bulk Insert. 

    # Create separate dictionary list with separate dictionaries.
    translatedDictList = list()
    for d in dictList:
        translatedDictList.append(d.copy())


    if table == 'ClaimHeader':
        for d in translatedDictList:

            # Convert Python Boolean to SQL Server Bit
            # This may not be necessary. Was required at one stage while trying to setup SQL Server Bulk Insert.
            # 05/12/2020 Update.
            # 1) This is Not Required for Execute or ExecuteMany, but works either way.
            # 2) This is Required for Bulk Insert.
            # Hence included.
                   
            if d['IsCurrentVersion'] == True:
                d['IsCurrentVersion'] = 1
            elif d['IsCurrentVersion'] == False:
                d['IsCurrentVersion'] = 0
            else:
                d['IsCurrentVersion'] = 1
                   
            if d['IsMultiRiskPolicy'] == True:
                d['IsMultiRiskPolicy'] = 1
            elif d['IsMultiRiskPolicy'] == False:
                d['IsMultiRiskPolicy'] = 0
            else:
                d['IsMultiRiskPolicy'] = None

            # Setup string literal translation of Database type DATE - 10 chars - 'YYYY MM DD'
            # Not sure if this is necessary or helpful, so currently commented out.

            # PolicyStartDate
            # if d['PolicyStartDate'] != None:
            #     d['PolicyStartDate'] = str(d['PolicyStartDate'])[:10]
            # else:
            #     d['PolicyStartDate'] = ''

            # # PolicyEndDate
            # if d['PolicyEndDate'] != None:
            #     d['PolicyEndDate'] = str(d['PolicyEndDate'])[:10]
            # else:
            #     d['PolicyEndDate'] = ''

            # # ReportedDate
            # if d['ReportedDate'] != None:
            #     d['ReportedDate'] = str(d['ReportedDate'])[:10]
            # else:
            #     d['ReportedDate'] = ''

            # Setup string literal translation of Database type SMALLDATETIME - 16 chars - 'YYYY MM DD HH:MM:SS'
            # Not sure if this is necessary or helpful, so as above, currently commented out.

            # DecisionDate
            # if d['DecisionDate'] != None:
            #     d['DecisionDate'] = str(d['DecisionDate'])[:19]
            # else:
            #     d['ReportedDate'] = ''


    if table == 'ClaimMotorDetail':
        for d in translatedDictList:
            
            if d['IsVehicleTotalLoss'] == True:
                d['IsVehicleTotalLoss'] = 1
            elif d['IsVehicleTotalLoss'] == False:
                d['IsVehicleTotalLoss'] = 0
            else:
                d['IsVehicleTotalLoss'] = None
                

            if d['IsDriverListed'] == True:
                d['IsDriverListed'] = 1
            elif d['IsDriverListed'] == False:
                d['IsDriverListed'] = 0
            else:
                d['IsDriverListed'] = None

            if d['IsTPInvolved'] == True:
                d['IsTPInvolved'] = 1
            elif d['IsTPInvolved'] == False:
                d['IsTPInvolved'] = 0
            else:
                d['IsTPInvolved'] = None


    if table == 'ClaimReserveMovement':
        for d in translatedDictList:
            
            if d['IsSystemCreated'] == True:
                d['IsSystemCreated'] = 1
            elif d['IsSystemCreated'] == False:
                d['IsSystemCreated'] = 0
            else:
                d['IsSystemCreated'] = None


    if table == 'ClaimPayment':
        for d in translatedDictList:
            
            if d['IsInvoice'] == True:
                d['IsInvoice'] = 1
            elif d['IsInvoice'] == False:
                d['IsInvoice'] = 0
            else:
                d['IsInvoice'] = None
            
            if d['XsCollectedOnInvoice'] == True:
                d['XsCollectedOnInvoice'] = 1
            elif d['XsCollectedOnInvoice'] == False:
                d['XsCollectedOnInvoice'] = 0
            else:
                d['XsCollectedOnInvoice'] = None


    if table == 'ClaimPaymentDetail':
        for d in translatedDictList:
            
            if d['IsTaxFree'] == True:
                d['IsTaxFree'] = 1
            elif d['IsTaxFree'] == False:
                d['IsTaxFree'] = 0
            else:
                d['IsTaxFree'] = None
            

    if table == 'ClaimPaymentHistory':
        for d in translatedDictList:
            
            if d['IsSystemCreated'] == True:
                d['IsSystemCreated'] = 1
            elif d['IsSystemCreated'] == False:
                d['IsSystemCreated'] = 0
            else:
                d['IsSystemCreated'] = None


    if table == 'ClaimRecovery':
        for d in translatedDictList:
            
            if d['IsInvoice'] == True:
                d['IsInvoice'] = 1
            elif d['IsInvoice'] == False:
                d['IsInvoice'] = 0
            else:
                d['IsInvoice'] = None

            if d['IsXsCollection'] == True:
                d['IsXsCollection'] = 1
            elif d['IsXsCollection'] == False:
                d['IsXsCollection'] = 0
            else:
                d['IsXsCollection'] = None

            if d['IsSalvage'] == True:
                d['IsSalvage'] = 1
            elif d['IsSalvage'] == False:
                d['IsSalvage'] = 0
            else:
                d['IsSalvage'] = None


    if table == 'ClaimRecoveryDetail':
        for d in translatedDictList:
            
            if d['IsTaxFree'] == True:
                d['IsTaxFree'] = 1
            elif d['IsTaxFree'] == False:
                d['IsTaxFree'] = 0
            else:
                d['IsTaxFree'] = None


    if table == 'ClaimRecoveryHistory':
        for d in translatedDictList:
            
            if d['IsSystemCreated'] == True:
                d['IsSystemCreated'] = 1
            elif d['IsSystemCreated'] == False:
                d['IsSystemCreated'] = 0
            else:
                d['IsSystemCreated'] = None


    return translatedDictList

