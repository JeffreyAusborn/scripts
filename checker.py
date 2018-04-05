import requests
import json
import os
import sys
import time
import datetime
import commands

def getTheDatas(buildNumber):
	r = requests.get('http://jenkins.corp.clover.com:8080/job/build-deploy-server/'+str(buildNumber)+'/api/json')
	if r.status_code == 200:
		rJson = r.json()
		deployTarget=rJson['actions'][0]['parameters'][2]['value']
		if 'stg1' in deployTarget:
			if rJson['result'] != None and 'SUCCESS' in rJson['result']:
				releaseDate=rJson['actions'][0]['parameters'][1]['value']
				releaseDate_=releaseDate.split('_')[1]
				timeStamp = datetime.datetime.fromtimestamp(int(rJson['timestamp'])/1000.0).strftime('%Y-%m-%d')
				year = timeStamp.split('-')[0]
				return releaseDate_, year
	return '', ''

def getLatestBuildNumber():
	r = requests.get('http://jenkins.corp.clover.com:8080/job/build-deploy-server/lastBuild/api/json')
	rJson = r.json()
	return rJson['number']

def main():
	buildNumber=8164
	releaseDate = ''
	tempDate = ''
	year = ''
	tempYear = ''
	while True:
		latestBuild = getLatestBuildNumber()
		if latestBuild >= buildNumber:
			releaseDate, year = getTheDatas(buildNumber)
			buildNumber+=1

		if len(releaseDate) > 0:
			if len(tempDate) > 0 and (tempDate != releaseDate):
				os.system('python getcsv.py '+tempDate+' '+tempYear)
			tempDate = releaseDate
			tempYear = year

			counter = int(str(datetime.datetime.now()).replace(' ',':').split(':')[2])
			while counter < 60:
				time.sleep(60)
				counter += 1

			leHour = str(datetime.datetime.now()).replace(' ',':').split(':')[1]
			if (int(leHour) == 18) and "ServerWebCut" in tempDate:
				os.system('python getcsv.py '+tempDate+' '+tempYear)


main()
