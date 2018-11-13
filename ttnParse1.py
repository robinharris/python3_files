import json
import csv
inFileName = "aq3_ttn.txt"
outFileName = "aq3_ttn_nov13.csv"
inFile = open (inFileName,"r")
outFile = open (outFileName,"w")
count = 0 # used to select every other line from the input file
for line in inFile:
        reportJson = json.loads(line) # convert a line from the file into JSON
        payloadRow = reportJson['payload_fields'] # select the payload fields
        metadataRow = reportJson['metadata'] # select metadata fields
        # this line selects the list of gateways and their fields
        gatewayRow = json.dumps(reportJson['metadata']['gateways']) 
        # Next convert the list of gateways into JSON.  We need to remove the square brackets at the beginning and end of the list to present a string 
        gatewayDict = json.loads(gatewayRow[1:-1])
        del gatewayDict['latitude'] # need to delete these two keys because they duplicate the payload ones
        del gatewayDict['longitude']
        payloadRow.update(reportJson)
        payloadRow.update(metadataRow) # merge the metadata into the payload dict
        payloadRow.update(gatewayDict) # merge the gatewayDict into payload dict
        # these are the fields we want in the CSV
        fieldnames = ['counter', 'latitude', 'longitude', 'volatiles', 'pm10', 'pm25', 'time', 'rssi','channel']
        writer = csv.DictWriter(outFile, fieldnames = fieldnames, extrasaction='ignore')
        writer.writerow(payloadRow)
inFile.close()
outFile.close()
