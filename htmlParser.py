import urllib.request   
from bs4 import BeautifulSoup

import json

def printY(y, data):
    if str(y.nextSibling).find("font-size") > 0 or str(y.nextSibling).replace(u'\xa0', u' ') == ' ':
        print("%s , %s" % (str(y.contents[0]) , str(y.nextSibling.nextSibling.contents[0]).strip()))
        data[str(y.contents[0])] = str(y.nextSibling.nextSibling.contents[0]).strip()
    else:
        print("%s , %s" % (str(y.contents[0]) , str(y.nextSibling).strip()))
        data[str(y.contents[0])] = str(y.nextSibling).replace(u'\xa0', u'').strip()

if __name__ == "__main__":
    print("Hello World!")
    req = urllib.request.Request("https://www.mz.co.kr/portfolio-items/2011applicationlg-u-plus/")
    data = urllib.request.urlopen(req).read()

    bs = BeautifulSoup(data, 'html.parser')

    divClassGrid4 = bs.find("div", {"class": "grid4 col"})
    
    tagP = divClassGrid4.find_all("p")

    chkList = ['PROJECT', 'CLIENT', 'TYPE', 'DEBUT DATE', 'Production Coordinator', 'Design, Animation', 'Storyboards, Animation', 'Lighting, Shading, Rendering', 'Animation, Modeling', 'Created']

    jsonData = {}

    data = {}

    idxTagP = 0
    for x in tagP:
        try:
            idxTagY = 0
            for y in x.contents:
                for z in chkList:
                    if str(y).find(z) > 1:
                        printY(y, data)
                        break
        except UnicodeEncodeError:
            print("Error : %d" % (idxTagP))
        finally:
            idxTagP += 1

    print(json.dumps(data))
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)