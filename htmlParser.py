import urllib.request   
from bs4 import Tag, NavigableString, BeautifulSoup

import json

def printY(y, jsonData):
	if str(y.nextSibling).find("font-size") > 0 or str(y.nextSibling).find("span style") > 0 or str(y.nextSibling).replace(u'\xa0', u' ') == ' ':
		#print("%s , %s" % (str(y.text) , str(y.nextSibling.nextSibling.text).strip()))
		if isinstance(str(y.nextSibling.nextSibling), Tag):
			jsonData[str(y.text).replace(u'\xa0', u'').strip()] = str(y.nextSibling.nextSibling.text).strip()
		elif isinstance(str(y.nextSibling.nextSibling), NavigableString):
			jsonData[str(y.text).replace(u'\xa0', u'').strip()] = str(y.nextSibling.nextSibling).replace(u'\xa0', u'').strip().strip()
	else:
        #print("%s , %s" % (str(y.text) , str(y.nextSibling).strip()))
		jsonData[str(y.text).replace(u'\xa0', u'').strip()] = str(y.nextSibling).replace(u'\xa0', u'').strip()

def getTag(bs):
	divClassGrid4 = bs.find("div", {"class": "grid4 col"})
			
	tagP = divClassGrid4.find_all("p")

	chkList = ['PROJECT', 'CLIENT', 'TYPE', 'DEBUT DATE', 'Production Coordinator', 'Design, Animation', 'Storyboards, Animation', 'Lighting, Shading, Rendering', 'Animation, Modeling', 'Created']

	jsonData["link"] = req.full_url
	scriptIdx = 1
	for x in tagP:
		try:
			if len(x.text.strip()) < 50:
				for y in x.contents:
					for z in chkList:
						if str(y).find(z) > 1:
							printY(y, jsonData)
							break
			else:
				jsonData["script%d" % scriptIdx] = x.text.strip()
				scriptIdx += 1
		except UnicodeEncodeError:
			print("Error : UnicodeEncodeError")
		finally:
			pass

def getImage(bs):
	divClassGrid8 = bs.find("div", {"class": "grid8 col"})

	tagImgs = divClassGrid8.find_all("img")

	imgIdx = 1
	for img in tagImgs:
		jsonData["image%d" % imgIdx] = img['src']
		imgIdx += 1

if __name__ == "__main__":
	print("Hello World!")

	linkTextFilePath = "D:\python\htmlParser\linkList.txt"

	linkFile = open(linkTextFilePath,'r')
	outData = []
	links = linkFile.readlines()
	linkFile.close()
	for link in links:
		try:
			req = urllib.request.Request(link.replace(u'\n', u''))
			reqData = urllib.request.urlopen(req).read()

			bs = BeautifulSoup(reqData, 'html.parser')

			jsonData = {}

			getTag(bs)
			getImage(bs)

			print(jsonData)
			outData.append(jsonData)

		except:
			print("error link : %s" % (req.full_url))
		finally:
			jsonData = {}

	#print(json.dumps(data))
	with open('data.json', 'w', encoding='utf-8') as outfile:
		json.dump(outData, outfile, ensure_ascii=False)