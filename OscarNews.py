# Run every 2 hours, check hacker news to see if there's anything about Oscars.
# Store all the Oscar news in SQL.
# At EOD, query SQL database and send Oscar news to Oscar
# Expose flask API to query Oscar news database with

import requests
import simplejson as json

topStoriesUrl = 'https://hacker-news.firebaseio.com/v0/topstories.json'

topStories = json.loads(requests.get(topStoriesUrl).text)

for story in topStories:
    OscarCount = 0
    storyUrl = 'https://hacker-news.firebaseio.com/v0/item/' + str(story) + '.json'
    storyInfo = json.loads(requests.get(storyUrl).text)
    if storyInfo.has_key('title'):
        OscarCount += storyInfo['title'].lower().count("oscar")
    if storyInfo.has_key('kids'):
        for comment in storyInfo['kids']:
            commentUrl = 'https://hacker-news.firebaseio.com/v0/item/' + str(comment) + '.json'
            commentInfo = json.loads(requests.get(commentUrl).text)
            if commentInfo.has_key('text'):
                OscarCount += commentInfo['text'].lower().count("oscar")
    # Do something about Oscar Count
    print OscarCount 
