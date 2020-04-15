from flask import Flask, request
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="oscarapi",
  passwd="password",
  database="oscar_news"
)
mycursor = mydb.cursor()

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    return "<h1>Oscar's API</h1><p>This is my project to build a simple flask API over GCP.</p><h2>Usage:</h2><p>lastweek: show titles captured from last week</p><p>yesterday: show titles captured from yesterday</p><p>?includeComments=True: include comment in item retrieval</p><p>?includeUrls=True: include url in item retrival</p>"

@app.route('/lastweek', methods=['GET'])
def lastweek():
    includeComments = request.args.get('includeComments')
    if includeComments == "True":
        mycursor.execute("SELECT * FROM oscar_news WHERE entry_time BETWEEN DATE_SUB(NOW(),INTERVAL 1 WEEK) AND NOW();")
    else:
        mycursor.execute("SELECT * FROM oscar_news WHERE parent_id IS NULL AND entry_time BETWEEN DATE_SUB(NOW(),INTERVAL 1 WEEK) AND NOW();")
    mypage = "<h3>hn_id,parent_id,content,entry_time</h3>"
    for line in mycursor.fetchall():
        includeUrls = request.args.get('includeUrls')
        if includeUrls == "True":
            hn_id = line[0]
            url = "https://news.ycombinator.com/item?id=" + str(hn_id)
            mypage += '<a href=' + str(url) + '>' + str(url) + "</a>"
        mypage += "<p>" + str(line) + "</p>"
    return mypage

@app.route('/yesterday', methods=['GET'])
def yesterday():
    includeComments = request.args.get('includeComments')
    if includeComments == "True":
        mycursor.execute("SELECT * FROM oscar_news WHERE entry_time BETWEEN DATE_SUB(NOW(),INTERVAL 1 DAY) AND NOW();")
    else:
        mycursor.execute("SELECT * FROM oscar_news WHERE parent_id IS NULL AND entry_time BETWEEN DATE_SUB(NOW(),INTERVAL 1 DAY) AND NOW();")
    mypage = "<h3>hn_id,parent_id,content,entry_time</h3>"
    for line in mycursor.fetchall():
        includeUrls = request.args.get('includeUrls')
        if includeUrls == "True":
            hn_id = line[0]
            url = "https://news.ycombinator.com/item?id=" + str(hn_id)
            mypage += '<a href=' + str(url) + '>' + str(url) + "</a>"
        mypage += "<p>" + str(line) + "</p>"
    return mypage


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



# let's give an option to specify wanting see actual url
# see weekly hn news
# include comments
# see daily hn news
# home let's you know the commands
