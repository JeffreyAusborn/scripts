import requests
import json
import os
import sys
import time
import datetime



newDate = sys.argv[1]
cutdate = sys.argv[1]
for char in cutdate:
	if char.isupper():
		newDate = newDate.replace(char, ' '+char)
newDate = newDate.replace(sys.argv[2], ' '+sys.argv[2])
cutDate = "'"+newDate+"'"
allDict = {'cycleId':{}}

r = requests.get('https://jira.dev.clover.com/rest/zapi/latest/zql/executeSearch?zqlQuery=fixVersion='+cutDate.replace(' ', '%20').replace("'", "%22")+'&offset=1', auth=('jeffrey.ausborn', '9ijn*UHB9ijn*UHB'))

if r.status_code == 200:

	rjson = r.json()
	versionName = rjson['executions'][0]['versionName']
	failedString = ''
	totalCounts = rjson['totalCount']
	print totalCounts
	count = 1

	while count <= totalCounts:
		for i in range(0, len(rjson['executions'])):
			cycleId = rjson['executions'][i]['cycleId']
			if cycleId not in allDict['cycleId']:
				allDict['cycleId'][cycleId] = {}
				allDict['cycleId'][cycleId]['status'] = {}
				allDict['cycleId'][cycleId]['priority'] = {}
				allDict['cycleId'][cycleId]['cycleName'] = rjson['executions'][i]['cycleName']

			if rjson['executions'][i]['status']['name'] in allDict['cycleId'][cycleId]['status']:
				allDict['cycleId'][cycleId]['status'][rjson['executions'][i]['status']['name']] += 1
			else:
				allDict['cycleId'][cycleId]['status'][rjson['executions'][i]['status']['name']] = 1

			if rjson['executions'][i]['status']['name'] == 'FAIL':
				failedString+= "*"+rjson['executions'][i]['cycleName']+"*: "+rjson['executions'][i]['issueSummary']+"\n"

			if rjson['executions'][i]['priority'] in allDict['cycleId'][cycleId]['priority']:
				allDict['cycleId'][cycleId]['priority'][rjson['executions'][i]['priority']] += 1
			else:
				allDict['cycleId'][cycleId]['priority'][rjson['executions'][i]['priority']] = 1

		count += 20
		r = requests.get('https://jira.dev.clover.com/rest/zapi/latest/zql/executeSearch?zqlQuery=fixVersion='+cutDate.replace(' ', '%20').replace("'", "%22")+'&offset='+str(count), auth=('jeffrey.ausborn', '9ijn*UHB9ijn*UHB'))
		rjson = r.json()

	allDict_View = [ (v, k) for k,v in allDict['cycleId'].iteritems()]
	allDict_View.sort(reverse=True)

	zephyString = '{"channel":"CA112NSGP","as_user":"True","attachments": [{"text": "*'+versionName+'*","fields": [{"title":"Total Tests","value":'+str(totalCounts)+', "short":"True"},'
	for v,k in allDict_View:
		vDict_View = [ (v1, k1) for k1,v1 in v.iteritems()]
		vDict_View.sort(reverse=True)
		for v1, k1 in vDict_View:
			if k1 == 'cycleName':
				zephyString+='{"title": "cycleName","value": "'+str(v1)+'" ,"short": False},'
			elif k1 == 'status':
				v1Dict_View = [ (v2, k2) for k2,v2 in v1.iteritems()]
				v1Dict_View.sort(reverse=True)
				for v2, k2 in v1Dict_View:
					zephyString+='{"title": "'+str(k2)+'","value": '+str(v2)+' ,"short": True},'
			else:
				v1Dict_View = [ (v2, k2) for k2,v2 in v1.iteritems()]
				v1Dict_View.sort(reverse=True)
				for v2, k2 in v1Dict_View:
					zephyString+='{"title": "'+str(k2)+'","value": '+str(v2)+' ,"short": True},'

	zephyString+='{"title": "What Failed","value": "'+failedString.replace('"', '\\"')+'","short": False}],"color": "#F35A00"}]}'
	with open('testZeph.txt', 'w') as tz:
		tz.write(zephyString)	

	os.system("./sendCurl.sh")

else:
	print "bad url"



