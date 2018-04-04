#coding=utf-8

import json
import codecs
from bs4 import BeautifulSoup
from extract_functions import *
import time
import datetime
import jieba.analyse

jieba.load_userdict("jieba/mydict.txt")
###########
# Input your process [month, start-date, end-date] here!
###########
dateList = creat_date_list("04",18,24)
startTime = datetime.datetime.now()
wbCount = 0

for date in dateList:
    thisDate = date
    datapath = "../WBTestdata/" + thisDate + "/"
    if os.path.exists(datapath):
        print "got data"
    else:
        print "Did not find this day´s data, next day!!"
        time.sleep(5)
        continue

    outputPath = "../WBDatabase/time"
    if not os.path.exists(outputPath):
        os.mkdir(outputPath)
    outputFile = outputPath + thisDate + ".txt"
    with open(outputFile, "a") as output:
        output.write("\n")

    list_dirs = os.walk(datapath)
    for root, dirs, files in list_dirs:
        for f in files:
            filename = f.decode("gbk").encode("UTF-8")
            thisfilepath = datapath + filename.decode("UTF-8")
            thisCountry = filename.split(thisDate)[0].decode("UTF-8")
            print "----------------------------------------------------------------------------------------------"
            print "Find one: ", json.dumps(filename, encoding="UTF-8", ensure_ascii=False)
            print "----------------------------------------------------------------------------------------------"

            with codecs.open(thisfilepath, "r", "utf-8") as thisfile:
                content = thisfile.read()
                try:
                    thisdata = json.loads(content)
                except Exception:
                    print "no data here!"
                #### creat_at
                try:
                    thisRequesttime = thisdata['cardlistInfo']['starttime']
                    for i in range(len(thisdata['cards'][0]['card_group'])):
                        itemKeyword = thisCountry
                        itemID = str(thisdata['cards'][0]['card_group'][i]['mblog']['id'])
                        itemCreat = thisdata['cards'][0]['card_group'][i]['mblog']['created_at'].encode("UTF-8")
                        #change format of time
                        itemCreatFormat = process_time(itemCreat,thisRequesttime)
                        itemRepostCount = str(thisdata['cards'][0]['card_group'][i]['mblog']['reposts_count'])

                        itemSource = puncfilter(thisdata['cards'][0]['card_group'][i]['mblog']['source'])
                        itemSource2 =itemSource.encode("UTF-8")
                        itemSourceUni = platformUni(itemSource2)
                        itemSourceSimp = platformSimp(itemSourceUni)

                        itemUser = thisdata['cards'][0]['card_group'][i]['mblog']['user']['screen_name']
                        itemText = thisdata['cards'][0]['card_group'][i]['mblog']['text']

                        soup = BeautifulSoup(itemText, "html.parser")
                        itemTextPretty = ""
                        for string in soup.stripped_strings:
                            itemTextPretty += string
                        print "Text: ", itemTextPretty

                        itemTextPretty = removepeople(itemTextPretty)
                        itemTextPretty = removeurl(itemTextPretty)

                        itemTextP = puncfilter(itemTextPretty)
                        extract = jieba.analyse.extract_tags(itemTextP, topK=5, withWeight=True, allowPOS=())
                        extractline = ""
                        for word in extract:
                            co = word[0]
                            extractline = extractline + " " + co

                        itemUserID = str(thisdata['cards'][0]['card_group'][i]['mblog']['user']['id'])
                        itemUserGender = str(thisdata['cards'][0]['card_group'][i]['mblog']['user']['gender'])
                        itemUserFollower = str(thisdata['cards'][0]['card_group'][i]['mblog']['user']['followers_count'])
                        dataLine = itemCreatFormat + "\t" + itemKeyword.encode("UTF-8") + "\t" + str(itemID)  + "\t" + str(itemRepostCount) + "\t" + itemSourceUni + "\t" + itemSourceSimp + "\t" +itemUser.encode("UTF-8") + "\t" + str(itemUserID) + "\t" + str(itemUserFollower) + "\t" + itemUserGender + "\t" +itemTextP.encode("UTF-8")+ "\t"+ extractline.encode("UTF-8") + '\n'

                        with open(outputFile,"a") as output:
                            output.write(dataLine)
                            wbCount += 1
                except Exception,e:
                    print e
                    print "No data in this file! Next!"
                    time.sleep(3)
                    continue

endTime = datetime.datetime.now()

print "Use Time: ", endTime - startTime
print "Process total WB: ", wbCount