# Run every 2 hours, check hacker news to see if there's anything about Oscars.
# Store all the Oscar news in SQL.
# At EOD, query SQL database and send Oscar news to Oscar
# Expose flask API to query Oscar news database with

import requests
import simplejson as json
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="oscarapi",
  passwd="password",
  database="oscar_news"
)

mycursor = mydb.cursor()

topStoriesUrl = 'https://hacker-news.firebaseio.com/v0/topstories.json'

topStories = json.loads(requests.get(topStoriesUrl).text)

def checkChildren(parentInfo, isOscarNews):
    # Recursively check children to find Oscar mentions
    childInfos = []
    for child in parentInfo['kids']:
        childUrl = 'https://hacker-news.firebaseio.com/v0/item/' + str(child) + '.json'
        childInfo = json.loads(requests.get(childUrl).text)
        if childInfo.has_key('kids'):
            currChildInfos, isOscarNews = checkChildren(childInfo, isOscarNews)
            childInfos += currChildInfos
        childInfos.append(childInfo)
        if childInfo.has_key('text') and 'oscar' in childInfo['text'].encode("utf-8").lower():
            isOscarNews = True
    return childInfos, isOscarNews


for story in topStories:
    isOscarNews = False
    storyUrl = 'https://hacker-news.firebaseio.com/v0/item/' + str(story) + '.json'
    storyInfo = json.loads(requests.get(storyUrl).text)
    if storyInfo.has_key('title') and 'oscar' in storyInfo['title'].encode("utf-8").lower():
        isOscarNews = True
    commentInfos = []
    if storyInfo.has_key('kids'):
        commentInfos, isOscarNews = checkChildren(storyInfo, isOscarNews)
    if isOscarNews and storyInfo.has_key('id'):
        date = datetime.date(datetime.now())
        # Don't do anything if the title is already stored in database
        mycursor.execute('SELECT hn_id FROM oscar_news WHERE hn_id = ' + str(storyInfo['id']) + ';')
        if len(mycursor.fetchall()):
            print "Story " + str(storyInfo['id']) + " already recorded in database"
            continue
        # try catch. If try fails, try adding without content
        try:
            mycursor.execute('INSERT INTO oscar_news (hn_id, content, entry_time) VALUES (' + str(storyInfo['id']) + ',"' + storyInfo['title'].encode("utf-8").replace('"','char(39)') + '","' + str(date) +  '");')
        except:
            try:
                # Maybe sql didn't like info in title
                mycursor.execute('INSERT INTO oscar_news (hn_id, entry_time) VALUES (' + str(storyInfo['id']) + ',"' + str(date) +  '");')
            except:
                # Things to think about: null story info, story info not dictionary, no keys id or title
                print "Bad data entry for title"
        for commentInfo in commentInfos:
            try:
                mycursor.execute('INSERT INTO oscar_news (hn_id, parent_id, content, entry_time) VALUES (' + str(commentInfo['id']) + ',' + str(commentInfo['parent']) + ',"' + commentInfo['text'].encode("utf-8").replace('"','char(39)') + '","' + str(date) +  '");')
            except:
                try:
                    # Maybe sql didn't like the info in text
                    mycursor.execute('INSERT INTO oscar_news (hn_id, parent_id, entry_time) VALUES (' + str(commentInfo['id']) + ',' + str(commentInfo['parent']) + ',"' + str(date) +  '");')
                except:
                    print "Bad data entry for comment"
        mydb.commit()
        print storyInfo

