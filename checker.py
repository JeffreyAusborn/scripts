import requests
import json
import os
import sys
import time
import datetime
import commands
from bs4 import BeautifulSoup

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

def getAppCutDate():
	r = requests.get("https://confluence.dev.clover.com/rest/api/content/18323351?expand=body.storage", auth=('jeffrey.ausborn','9ijn*UHB9ijn*UHB'))
	rjson = r.json()

	html_string = rjson['body']['storage']['value']
	soup = BeautifulSoup(html_string, 'lxml') # Parse the HTML as a string
	table = soup.find_all('table')[0] # Grab the first table

	row_marker = 0
	for row in table.find_all('tr')[0]:
	    if "CUT:" in row:
	        continue
	    else:
	        return row.get_text()+" Apps Cut"

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
			appDate = getAppCutDate()
			if tempDate != releaseDate:
				os.system('python getcsv.py '+releaseDate+' '+year)
				if len(appDate) > 0:
					os.system('python getcsv.py '+appDate.replace(' ', '')+' '+year)
				tempDate = releaseDate
				tempYear = year


		leHour = str(datetime.datetime.now()).replace(' ',':').split(':')[1]
		if (int(leHour) == 17) and "ServerWebCut" in tempDate:
			os.system('python getcsv.py '+tempDate+' '+tempYear)
			appDate = getAppCutDate()
			if len(appDate) > 0:
				os.system('python getcsv.py '+appDate.replace(' ', '')+' '+tempYear)
		elif int(leHour) == 16:
			counter = int(str(datetime.datetime.now()).replace(' ',':').split(':')[2])
			while counter < 60:
				time.sleep(60)
				counter += 1
		else:
			time.sleep(60)



main()
