#!/usr/bin/python
import csv
import math
import sys


def endPointCSV(getAPI, divBy):
    apiCsv = 'endpoints.csv'
    with open(apiCsv, 'w') as csvfile:
        fieldnames = ['Type', 'Request', 'Avg OPS']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        getAPI_view = [(v, k) for k, v in getAPI.iteritems()]
        getAPI_view.sort(reverse=True)
        for v, k in getAPI_view:
            kSplit = k.split(' ')
            writer.writerow({'Type': kSplit[0], 'Request': kSplit[1], 'Avg OPS': int(math.ceil(v/(divBy)*1.0))})


def kibanaParser(csvFilename, apiDict, apiType):
    with open(csvFilename, 'rb') as csvfile:
        apiReader = csv.DictReader(csvfile)
        for row in apiReader:
            if apiType+" "+row['pattern.raw: Descending'] in apiDict:
                apiDict[apiType+" "+row['pattern.raw: Descending']] += int(row['Count'])
            else:
                apiDict[apiType+" "+row['pattern.raw: Descending']] = int(row['Count'])
    print len(apiDict)


def regularParser(csvFilename, apiDict, apiType):
    with open(csvFilename, 'rb') as csvfile:
        apiReader = csv.DictReader(csvfile)
        for row in apiReader:
            if len(row['Request']) > 0:
                if apiType+" "+row['Request'] in apiDict:
                    apiDict[apiType+" "+row['Request']] += int(row['OPS'])
                else:
                    apiDict[apiType+" "+row['Request']] = int(row['OPS'])
    print len(apiDict)


def main():
    getAPI = {}
    if sys.argv[2] == "1":
        kibanaParser(sys.argv[1], getAPI, "GET")
        endPointCSV(getAPI, 3600)
    else:
        regularParser(sys.argv[1], getAPI, "GET")
        endPointCSV(getAPI, 1)


main()
