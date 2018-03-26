import requests
import datetime
import time
import os

months = {'Jan':"01", 'Feb':"02", 'Mar':"03", 'Apr':"04", 'May':"05", 'Jun':"06", 'Jul':"07", 'Aug':"08", 'Sep':"09", 'Oct':"10", 'Nov':"11", 'Dec':"12"}
def monthToNum(abbrMonth):
	global months
	if abbrMonth in months: 
		return months[abbrMonth]


def getTheData(buildNumber):
	r = requests.get('http://jenkins.corp.clover.com:8080/job/build-deploy-server/'+str(buildNumber)+'/api/json')
	if r.status_code == 200:
		rJson = r.json()
		deployTarget=rJson['actions'][0]['parameters'][2]['value']
		if 'stg1' in deployTarget:
			if rJson['result'] != None and 'SUCCESS' in rJson['result']:
				releaseDate=rJson['actions'][0]['parameters'][1]['value']
				releaseDate_=releaseDate.replace('ServerWebCut', '').split('_')[1]
				# result = ''.join(i for i in releaseDate_ if not i.isdigit()) 
				timeStamp = datetime.datetime.fromtimestamp(int(rJson['timestamp'])/1000.0).strftime('%Y-%m-%d')
    			os.system("./selectCutData.sh "+releaseDate_+" "+timeStamp)

def getLatestBuildNumber():
	r = requests.get('http://jenkins.corp.clover.com:8080/job/build-deploy-server/lastBuild/api/json')
	rJson = r.json()
	return rJson['number']

def main():
	buildNumber=8028
	while True:
		latestBuild = getLatestBuildNumber()
		if latestBuild != buildNumber:
			getTheData(buildNumber)
			buildNumber+=1
		else:
			getTheData(buildNumber)
		time.sleep(1)

main()