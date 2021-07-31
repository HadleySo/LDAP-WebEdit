from flask import render_template, request
from LEdit import app

@app.route('/',methods = ['POST', 'GET'])
def index(name=None):
    print("INFO: Incoming request at root " + request.method)
    return render_template('index.html')    


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
