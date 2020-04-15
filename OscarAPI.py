from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Oscar's API</h1><p>This is my project to build a simple flask API over GCP.</p><h2>Usage:</h2><p>lastweek: show titles captured from last week</p><p>yesterday: show titles captured from yesterday</p><p>?includeComment: include comment in item retrieval</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



# let's give an option to specify wanting see actual url
# see weekly hn news
# include comments
# see daily hn news
# home let's you know the commands
