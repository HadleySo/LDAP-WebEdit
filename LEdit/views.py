from flask import render_template, request
from LEdit import app

@app.route('/',methods = ['POST', 'GET'])
def index(name=None):
    print("INFO: Incoming request at root " + request.method)

    if request.method == 'POST':
        # Request to create config or request to abort config creation
        if request.form.get('MainConfig'):
            print("INFO: POST request to Edit Config")
            return render_template('config.html')
        if request.form.get('cancelConfigEdit'):
            print("INFO: POST request to go cancel config edit")
            return render_template('index.html', blueMessage = "Config edit canceled")
    
    return render_template('index.html')    

@app.route('/editConfig',methods = ['POST', 'GET'])
def config(name=None):
    print("INFO: Incoming request at /editConfig " + request.method)
    if request.method == 'POST':
        from .appActions import createConfig
        configResult = createConfig.main(request)
        if (configResult == False):
            return render_template('index.html', blueMessage = "ERROR in creating config")
        if (configResult == True):
            return render_template('index.html', blueMessage = "Success in creating config")

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
