from flask import render_template, request, redirect
from flask.helpers import url_for
from LEdit import app


@app.route('/', methods=['POST', 'GET'])
def index(name=None):
    print("INFO: Incoming request at root " + request.method)

    if request.method == 'POST':
        # Request to create config or request to abort config creation
        if request.form.get('MainConfig'):
            print("INFO: POST request to Edit Config")

            from .appActions import createConfig, customLocale
            currentConfig = createConfig.getConfig()
            currentConfigDict = createConfig.getConfigDict()
            localOptions = customLocale.getAll()

            return render_template('config.html',
                                   currentConfig=currentConfig,
                                   currentConfigDict=currentConfigDict,
                                   localOptions=localOptions)

        if request.form.get('AddEntry'):
            print("INFO: POST request to Add Entries")

            # Get DN Base names if possible
            from .appActions import searchLDAP, customLocale
            names = searchLDAP.getBaseName()
            BaseOne, BaseTwo = "", ""
            if not (names == False):
                BaseOne = ": " + names[0]
                BaseTwo = ": " + names[1]

            localOptions = customLocale.getAll()

            return render_template('add.html', baseOneName=BaseOne, baseTwoName=BaseTwo, localOptions=localOptions)

        if request.form.get('SearchEntry'):
            print("INFO: POST request to Search Entries")

            # Get DN Base names if possible
            from .appActions import searchLDAP, customLocale
            names = searchLDAP.getBaseName()
            BaseOne, BaseTwo = "", ""
            if not (names == False):
                BaseOne = ": " + names[0]
                BaseTwo = ": " + names[1]

            localOptions = customLocale.getAll()

            return render_template('search.html', baseOneName=BaseOne, baseTwoName=BaseTwo, searchTable=None, localOptions=localOptions)

        if request.form.get('DelEntry'):
            print("INFO: POST request to Delete Entries")

            # Get DN Base names if possible
            from .appActions import searchLDAP, customLocale
            names = searchLDAP.getBaseName()
            BaseOne, BaseTwo = "", ""
            if not (names == False):
                BaseOne = ": " + names[0]
                BaseTwo = ": " + names[1]

            localOptions = customLocale.getAll()

            return render_template('delete.html', baseOneName=BaseOne, baseTwoName=BaseTwo, searchTable=None, localOptions=localOptions)

        if request.form.get('SendSMS'):
            print("INFO: POST request to Send SMS")
            from .appActions import sendMessage, customLocale
            localOptions = customLocale.getAll()
            rooms = sendMessage.getExt()

            if (rooms != False):
                return render_template('sendSMS.html', localOptions=localOptions, roomList=rooms)
            else:
                return render_template('index.html', blueMessage="Error in getting extestions", localOptions=localOptions)


        from .appActions import customLocale
        localOptions = customLocale.getAll()
        if request.form.get('cancelConfigEdit'):
            print("INFO: POST request to go cancel config edit")
            return render_template('index.html', blueMessage="Config edit canceled", localOptions=localOptions)
        if request.form.get('cancelSearch'):
            print("INFO: POST request to go cancel search")
            return render_template('index.html', blueMessage="LDAP search canceled", localOptions=localOptions)
        if request.form.get('cancelAdd'):
            print("INFO: POST request to go cancel add")
            return render_template('index.html', blueMessage="LDAP add canceled", localOptions=localOptions)
        if request.form.get('cancelDelete'):
            print("INFO: POST request to go cancel delete")
            return render_template('index.html', blueMessage="LDAP delete canceled", localOptions=localOptions)
        if request.form.get('cancelSMS'):
            print("INFO: POST request to go cancel SMS")
            return render_template('index.html', blueMessage="SMS message canceled", localOptions=localOptions)

    from .appActions import customLocale
    localOptions = customLocale.getAll()
    return render_template('index.html', localOptions=localOptions)


@app.route('/editConfig', methods=['POST', 'GET'])
def config(name=None):
    print("INFO: Incoming request at /editConfig " + request.method)
    if request.method == 'POST':
        from .appActions import createConfig, customLocale
        configResult = createConfig.main(request)
        localOptions = customLocale.getAll()
        if (configResult == False):
            return render_template('index.html', blueMessage="ERROR in creating config", localOptions=localOptions)
        if (configResult == True):
            return render_template('index.html', blueMessage="Success in creating config", localOptions=localOptions)


@app.route('/search', methods=['POST', 'GET'])
def search(name=None):
    print("INFO: Incoming request at /search " + request.method)
    if request.method == 'POST':
        from .appActions import searchLDAP, customLocale
        querryResults = searchLDAP.searchQuerryFull(request)
        localOptions = customLocale.getAll()

        names = searchLDAP.getBaseName()  # Get DN Base names if possible
        BaseOne, BaseTwo = "", ""
        if not (names == False):
            BaseOne = ": " + names[0]
            BaseTwo = ": " + names[1]

        print("Full querry results: ")
        print(querryResults)
        if querryResults[0] == False:    # Search failed
            return render_template('search.html',
                                   baseOneName=BaseOne,
                                   baseTwoName=BaseTwo,
                                   blueMessage=querryResults[1],
                                   searchResults="ERROR - Unable to complete search",
                                   localOptions=localOptions)

        if querryResults[0] == True:
            tableResults = searchLDAP.resultCleaner(querryResults[2])
            print(tableResults)

            if tableResults[0] == True:
                return render_template('search.html',
                                       baseOneName=BaseOne,
                                       baseTwoName=BaseTwo,
                                       searchResults="Search successful",
                                       searchTable=tableResults[1],
                                       localOptions=localOptions)
            # Search worked, but issue with result cleaner
            elif tableResults[0] == False:
                return render_template('search.html',
                                       baseOneName=BaseOne,
                                       baseTwoName=BaseTwo,
                                       searchResults=str(tableResults[1]),
                                       searchTable=None,
                                       localOptions=localOptions)


@app.route('/add', methods=['POST', 'GET'])
def add(name=None):
    print("INFO: Incoming request at /add " + request.method)
    if request.method == 'POST':
        from .appActions import addLDAP, customLocale
        addResult = addLDAP.main(request)
        localOptions = customLocale.getAll()

        if (addResult[0] == False):
            message = "ERROR in adding LDAP entry" + str(addResult[1])
            return redirect(url_for(".requestSent", blueMessage=message))

        if (addResult[0] == True):
            message = "Success! - " + str(addResult[1])
            return redirect(url_for(".requestSent", blueMessage=message))


@app.route('/deleteSearch', methods=['POST', 'GET'])
def deleteSearch(name=None):
    print("INFO: Incoming request at /deleteSearch " + request.method)
    if request.method == 'POST':
        from .appActions import searchLDAP, deleteLDAP, customLocale
        querryResults = searchLDAP.searchQuerryFull(request)
        localOptions = customLocale.getAll()

        names = searchLDAP.getBaseName()  # Get DN Base names if possible
        BaseOne, BaseTwo = "", ""
        if not (names == False):
            BaseOne = ": " + names[0]
            BaseTwo = ": " + names[1]

        print("Full querry results: ")
        print(querryResults)

        if querryResults[0] == False:    # Search failed
            return render_template('delete.html',
                                   baseOneName=BaseOne,
                                   baseTwoName=BaseTwo,
                                   blueMessage=querryResults[1],
                                   searchResults="ERROR - Unable to complete search",
                                   localOptions=localOptions)
        if querryResults[0] == True:
            tableResults = searchLDAP.resultCleaner(querryResults[2])
            fullDNlist = deleteLDAP.resultDNSorter(querryResults[2])

            print("Table Results:")
            print(tableResults)
            print("Full DN List")
            print(fullDNlist)

            if tableResults[0] == True:
                return render_template('delete.html',
                                       baseOneName=BaseOne,
                                       baseTwoName=BaseTwo,
                                       searchResults="Search successful",
                                       searchTable=tableResults[1],
                                       DNlist=fullDNlist,
                                       localOptions=localOptions)
            # Search worked, but issue with result cleaner
            elif tableResults[0] == False:
                return render_template('delete.html',
                                       baseOneName=BaseOne,
                                       baseTwoName=BaseTwo,
                                       searchResults=str(tableResults[1]),
                                       searchTable=None,
                                       localOptions=localOptions)


@app.route('/deleteEntry', methods=['POST', 'GET'])
def deleteEntry(name=None):
    print("INFO: Incoming request at /deleteEntry " + request.method)
    print(request.form)

    from .appActions import customLocale
    localOptions = customLocale.getAll()

    if request.method == 'POST':
        return render_template('deleteConfirm.html',
                               entryInfo=request.form['deleteEntry'],
                               localOptions=localOptions)


@app.route('/deleteEntryConfirmed', methods=['POST', 'GET'])
def deleteEntryConfirmed(name=None):
    print("INFO: Incoming request at /deleteEntry " + request.method)
    print(request.form)

    if request.method == 'POST':
        from .appActions import deleteLDAP, customLocale
        deleteResult = deleteLDAP.deleteRequesetFull(
            request.form['deleteConfirmed'])

        if deleteResult[0] == False:
            message = deleteResult[1]
            return redirect(url_for(".requestSent", blueMessage=message))

        elif deleteResult[0] == True:
            message = "Successfully deleted:   " + request.form['deleteConfirmed']
            return redirect(url_for(".requestSent", blueMessage=message))

@app.route('/sendSMS', methods=['POST', 'GET'])
def sendSMS(name=None):
    print("INFO: Incoming request at /sendSMS " + request.method)
    print(request.form)

    if request.method == 'POST':
        from .appActions import sendMessage, customLocale

        sendResponse = sendMessage.sendTextMessage(request)

        if (sendResponse[0] == False):
            message = "MESSAGE SEND FAILURE - " + str(sendResponse[1])
            return redirect(url_for(".requestSent", blueMessage=message))
        if (sendResponse[0] == True):
            message = "Message sent successfully - " + str(sendResponse[1])
            return redirect(url_for(".requestSent", blueMessage=message))
        else:
            message = "MESSAGE SEND FAILURE - Unknown error!"
            return redirect(url_for(".requestSent", blueMessage=message))

@app.route('/requestSent', methods=['GET'])
def requestSent(name=None):
    from .appActions import customLocale
    localOptions = customLocale.getAll()

    bMessage= request.args.get('blueMessage')

    return render_template('index.html', blueMessage=bMessage, localOptions=localOptions)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
