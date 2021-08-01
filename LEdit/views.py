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
        if request.form.get('AddEntry'):
            print("INFO: POST request to Add Entries")

            from .appActions import searchLDAP              # Get DN Base names if possible
            names = searchLDAP.getBaseName()
            BaseOne, BaseTwo = "", ""
            if not (names == False):
                BaseOne = ": " + names[0]
                BaseTwo = ": " + names[1]
        
            return render_template('add.html', baseOneName = BaseOne, baseTwoName = BaseTwo)

        if request.form.get('SearchEntry'):
            print("INFO: POST request to Search Entries")

            from .appActions import searchLDAP              # Get DN Base names if possible
            names = searchLDAP.getBaseName()
            BaseOne, BaseTwo = "", ""
            if not (names == False):
                BaseOne = ": " + names[0]
                BaseTwo = ": " + names[1]
        
            return render_template('search.html', baseOneName = BaseOne, baseTwoName = BaseTwo, searchTable = None)
        
        if request.form.get('DelEntry'):
            print("INFO: POST request to Delete Entries")

            from .appActions import searchLDAP              # Get DN Base names if possible
            names = searchLDAP.getBaseName()
            BaseOne, BaseTwo = "", ""
            if not (names == False):
                BaseOne = ": " + names[0]
                BaseTwo = ": " + names[1]
        
            return render_template('delete.html', baseOneName = BaseOne, baseTwoName = BaseTwo, searchTable = None)

        if request.form.get('cancelConfigEdit'):
            print("INFO: POST request to go cancel config edit")
            return render_template('index.html', blueMessage = "Config edit canceled")
        if request.form.get('cancelSearch'):
            print("INFO: POST request to go cancel search")
            return render_template('index.html', blueMessage = "LDAP search canceled")
        if request.form.get('cancelAdd'):
            print("INFO: POST request to go cancel add")
            return render_template('index.html', blueMessage = "LDAP add canceled")
        if request.form.get('cancelDelete'):
            print("INFO: POST request to go cancel delete")
            return render_template('index.html', blueMessage = "LDAP delete canceled")
    
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

@app.route('/search',methods = ['POST', 'GET'])
def search(name=None):
    print("INFO: Incoming request at /search " + request.method)
    if request.method == 'POST':
        from .appActions import searchLDAP
        querryResults = searchLDAP.searchQuerryFull(request)
            
        names = searchLDAP.getBaseName()  # Get DN Base names if possible
        BaseOne, BaseTwo = "", ""
        if not (names == False):
            BaseOne = ": " + names[0]
            BaseTwo = ": " + names[1]
        
        print("Full querry results: ")
        print(querryResults)
        if querryResults[0] == False:    # Search failed
            return render_template('search.html', baseOneName = BaseOne, baseTwoName = BaseTwo, blueMessage = querryResults[1], searchResults = "ERROR - Unable to complete search")
        if querryResults[0] == True:
            tableResults = searchLDAP.resultCleaner(querryResults[2])
            print(tableResults)

            if tableResults[0] == True:
                return render_template('search.html', baseOneName = BaseOne, baseTwoName = BaseTwo, searchResults = "Search successful", searchTable = tableResults[1])
            elif tableResults[0] == False:
                return render_template('search.html', baseOneName = BaseOne, baseTwoName = BaseTwo, searchResults = str(tableResults[1]), searchTable = None)        

@app.route('/add',methods = ['POST', 'GET'])
def add(name=None):
    print("INFO: Incoming request at /add " + request.method)
    if request.method == 'POST':
        from .appActions import addLDAP
        addResult = addLDAP.main(request)
        if (addResult[0] == False):
            from .appActions import searchLDAP              # Get DN Base names if possible
            names = searchLDAP.getBaseName()
            BaseOne, BaseTwo = "", ""
            if not (names == False):
                BaseOne = ": " + names[0]
                BaseTwo = ": " + names[1]

            return render_template('add.html', blueMessage = "ERROR in adding LDAP entry", addResults = addResult[1], baseOneName = BaseOne, baseTwoName = BaseTwo)
        if (addResult[0] == True):
            return render_template('add.html', blueMessage = "Success!", addResults = addResult[1])

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
