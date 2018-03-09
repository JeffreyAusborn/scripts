import os
import sys
import json
import requests

dict1 = {}
urlScore = {}
jsCSS = {}
images = {}

f = open('outputWeb.txt', 'r')
cloverUrl = ""
foo = 0

# "Getting optimization scores for web. **** If URL requires Login, then scores will be based on Login page, not the page itself ****"

# "If a URL says it can be optimized and doesn't show any items, that represents a repeated item."

for line in f:
	if "/m/" in line:
		continue
	if foo >= 10:
		break
	if "First" in line and not line[20:len(line)-1] in cloverUrl:
		foo += 1
		cloverUrl = line[20:len(line)-1]
		print ""



		url = 'https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url='+cloverUrl+'&key='+sys.argv[1]


		resp = requests.get(url=url)
		# resp1 = requests.get(url=cloverUrl)
		data = json.loads(resp.text)
		
		# print data
		# print json.dumps(data, sort_keys=True, indent=4)
		print cloverUrl+" could be optimized by doing the following."
		urlScore[cloverUrl] = str(data['ruleGroups']['SPEED']['score'])

		# print data['formattedResults']['ruleResults']['OptimizeImages']


		i = 0
		# print "   Seeking optimization scores >= 10%"
		for datas in data['formattedResults']['ruleResults']:
			optimizationScore = data['formattedResults']['ruleResults'][datas]['ruleImpact']
			if optimizationScore >= 10:
				dict1[datas] = optimizationScore
				if "OptimizeImages" in datas:
					print "\"your page has \""+str(len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls']))+"\" images that can be optimized.\""
					for i in range(0, len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'])):
						# print "Can reduced the size of images by a total of "+str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['header']['args'][2]['value'], sort_keys=True, indent=4))
						# print len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'])
						# imagePerc = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['header']['args'][2]['value'], sort_keys=True, indent=4))
						imageUrl = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'][i]['result']['args'][0]['value'], sort_keys=True, indent=4))
						if not imageUrl in images:
							images[imageUrl] = 1
							imageSaveBytes = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'][i]['result']['args'][1]['value'], sort_keys=True, indent=4))
							imagePerc = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'][i]['result']['args'][2]['value'], sort_keys=True, indent=4))
							formatImg = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'][i]['result']['format'], sort_keys=True, indent=4))
							print "   "+formatImg.replace('{{URL}}', imageUrl).replace('{{SIZE_IN_BYTES}}', imageSaveBytes).replace('{{PERCENTAGE}}', imagePerc)
						else:
							images[imageUrl] = images[imageUrl] + 1
						
				if "MinimizeRenderBlockingResources" in datas:
					# print "MinimizeRenderBlockingResources len : "+str(len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'])+len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls']))
					numScripts = str(json.dumps(data['formattedResults']['ruleResults'][datas]['summary']['args'][0]['value'], sort_keys=True, indent=4))
					numCSS = str(json.dumps(data['formattedResults']['ruleResults'][datas]['summary']['args'][1]['value'], sort_keys=True, indent=4))
					formatRender = str(json.dumps(data['formattedResults']['ruleResults'][datas]['summary']['format'], sort_keys=True, indent=4))
					print formatRender.replace('{{NUM_SCRIPTS}}', numScripts).replace('{{NUM_CSS}}', numCSS)
					for i in range (0, len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'])):
						if not str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value']) in jsCSS:
							jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])] = 1
							print "   "+str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])
						else:
							jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])] = jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])]+1
							print "   "+str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])
					for i in range (0, len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'])):
						if not str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value']) in jsCSS:
							jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])] = 1
							print "   "+str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])
						else:
							jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])] = jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])]+1
						print "   "+str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])



				# print datas+" has a score of "+str(optimizationScore)
				# print ""
		# print dict1


		# dict1_view = [ (v, k) for k,v in dict1.iteritems()]
		# dict1_view.sort(reverse=True)
		# for v,k in dict1_view:
		# 	print "%s: %d" % (k,v)

		dict1 = {}
	if "Recursing" in line and not line[19:len(line)-1] in cloverUrl:
		foo += 1
		cloverUrl = line[19:len(line)-1]
		print ""
		# print cloverUrl



		url = 'https://www.googleapis.com/pagespeedonline/v2/runPagespeed?url='+cloverUrl+'&key='+sys.argv[1]


		resp = requests.get(url=url)
		# resp1 = requests.get(url=cloverUrl)
		data = json.loads(resp.text)
		
		# print data
		# print json.dumps(data, sort_keys=True, indent=4)
		print cloverUrl+" could be optimized by doing the following."
		urlScore[cloverUrl] = str(data['ruleGroups']['SPEED']['score'])
		# print data['formattedResults']['ruleResults']['OptimizeImages']


		i = 0
		# print "----- Seeking optimization scores >= 10% -----"
		for datas in data['formattedResults']['ruleResults']:
			optimizationScore = data['formattedResults']['ruleResults'][datas]['ruleImpact']
			if optimizationScore >= 10:
				dict1[datas] = optimizationScore
				if "OptimizeImages" in datas:
					print "\"Your page has \""+str(len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls']))+"\" images that can be optimized.\""
					for i in range(0, len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'])):
						# print "Can reduced the size of images by a total of "+str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['header']['args'][2]['value'], sort_keys=True, indent=4))
						# print len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'])
						# imagePerc = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['header']['args'][2]['value'], sort_keys=True, indent=4))
						imageUrl = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'][i]['result']['args'][0]['value'], sort_keys=True, indent=4))
						if not imageUrl in images:
							images[imageUrl] = 1
							imageSaveBytes = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'][i]['result']['args'][1]['value'], sort_keys=True, indent=4))
							imagePerc = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'][i]['result']['args'][2]['value'], sort_keys=True, indent=4))
							formatImg = str(json.dumps(data['formattedResults']['ruleResults'][datas]['urlBlocks'][0]['urls'][i]['result']['format'], sort_keys=True, indent=4))
							print "   "+formatImg.replace('{{URL}}', imageUrl).replace('{{SIZE_IN_BYTES}}', imageSaveBytes).replace('{{PERCENTAGE}}', imagePerc)
						else:
							images[imageUrl] = images[imageUrl] + 1
				if "MinimizeRenderBlockingResources" in datas:
					# print "MinimizeRenderBlockingResources len : "+str(len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'])+len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls']))
					numScripts = str(json.dumps(data['formattedResults']['ruleResults'][datas]['summary']['args'][0]['value'], sort_keys=True, indent=4))
					numCSS = str(json.dumps(data['formattedResults']['ruleResults'][datas]['summary']['args'][1]['value'], sort_keys=True, indent=4))
					formatRender = str(json.dumps(data['formattedResults']['ruleResults'][datas]['summary']['format'], sort_keys=True, indent=4))
					print formatRender.replace('{{NUM_SCRIPTS}}', numScripts).replace('{{NUM_CSS}}', numCSS)
					for i in range (0, len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'])):
						if not str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value']) in jsCSS:
							jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])] = 1
							print "   "+str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])
						else:
							jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])] = jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])]+1
							print "   "+str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][1]['urls'][i]['result']['args'][0]['value'])
					for i in range (0, len(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'])):
						if not str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value']) in jsCSS:
							jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])] = 1
							print "   "+str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])
						else:
							jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])] = jsCSS[str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])]+1
							print "   "+str(data['formattedResults']['ruleResults'][datas]['urlBlocks'][2]['urls'][i]['result']['args'][0]['value'])
				# print datas+" has a score of "+str(optimizationScore)
				# print ""
		# print dict1


		# dict1_view = [ (v, k) for k,v in dict1.iteritems()]
		# dict1_view.sort(reverse=True)
		# for v,k in dict1_view:
		# 	print "%s: %d" % (k,v)

		dict1 = {}




print ""
print "Item : Count"
images_view = [ (v, k) for k,v in images.iteritems()]
images_view.sort(reverse=True)
for v,k in images_view:
	print "%s : %d" % (k,v)

print ""
print "Item : Count"
jsCSS_view = [ (v, k) for k,v in jsCSS.iteritems()]
jsCSS_view.sort(reverse=True)
for v,k in jsCSS_view:
	print "%s : %d" % (k,v)



print ""
print "List of (URL : Scores) - Lower the score, the more the page can be optimized"
urlScore_view = [ (v, k) for k,v in urlScore.iteritems()]
urlScore_view.sort(reverse=False)
for v,k in urlScore_view:
	print "%s : %s" % (k,v)





# for bar in dict2:
# 	print bar+" : "+dict2[bar]
# print json.dumps(data['formattedResults']['ruleResults']['OptimizeImages'], sort_keys=True, indent=4)


