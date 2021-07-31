import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")

def getBaseName():
    print("INFO: Trying to get SearchBase names")
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
        names = []
        names.append(cfg.get('LDAP','searchbaseone-name'))
        names.append(cfg.get('LDAP','searchbasetwo-name'))
        return names
    except Exception as e:
        print("[WARNING] Failed to read names from config file")
        print(str(e))
        return False

def editRequesetFull(request):
    from . import connections

    # Connect and Bind to LDAP server
    conn = connections.connect()
    if conn == None:
        print("[ERROR] Search failed due to failed connection")
        querryResult = [False, "[ERROR] Search failed due to failed connection"]
        return querryResult
    bindResult = connections.bind(conn)
    if not (bindResult == None):
        connections.disconnect(conn)
        querryResult = [False, bindResult]
        return querryResult
        
def searchQuerryFull(request):
    from . import connections

    print("INFO: Beginning to querry LDAP server")
    print(request.form)

    # Connect and Bind to LDAP server
    conn = connections.connect()
    if conn == None:
        print("[ERROR] Search failed due to failed connection")
        querryResult = [False, "[ERROR] Search failed due to failed connection"]
        return querryResult
    
    # Pull config for DN Search Bases
    cfg = configparser.ConfigParser()
    cfg.read(configPathFull)
    
    dn = ""                                                         # The DN search base
    attr_name = ['cn', 'sn', 'telephoneNumber', 'description']      # What attributes to show in results
    searchStr = request.form['searchString']

    # Set attributes based on form
    if request.form['searchBase'] == 'baseOne':
        dn = cfg.get('LDAP','searchbaseone').strip()
    elif request.form['searchBase'] == 'baseTwo':
        dn = cfg.get('LDAP','searchbasetwo').strip()

    if request.form['searchField'] == 'notes':
        searchFilter = "(&(objectclass=person)(description=" + searchStr + "))"
    elif request.form['searchField'] == 'pNum':
        searchFilter = "(&(objectclass=person)(telephoneNumber=" + searchStr + "))"
    elif request.form['searchField'] == 'lName':
        searchFilter = "(&(objectclass=person)(sn=" + searchStr + "))"
    elif request.form['searchField'] == 'fName':
        searchFilter = "(&(objectclass=person)(cn=" + searchStr + "))"
    
    print(searchFilter)
    
    # Execute search
    try:
        import ldap
        successResults = conn.search_s( dn, ldap.SCOPE_SUBTREE, searchFilter, attr_name )
        if len(successResults) == 0:
            successResults = "Your querry had no matches"
        querryResult = [True, None, successResults]
        connections.disconnect(conn)
        return querryResult
    except Exception as e:
        connections.disconnect(conn)
        print("[ERROR] Unable to complete search.")
        querryResult = [False, "[ERROR] Unable to complete search. " + str(e)]
        return querryResult

def resultCleaner(results):
    print("INFO: Cleaning LDAP search results")
    if not isinstance(results, list):
        print("INFO: resultCleaner input was not a list" + str(type(results)))
        rtnList = [False, results, "resultCleaner input was not a list" + str(type(results))]
        return rtnList
    if results == None:
        print("INFO: resultCleaner input was a None value")
        rtnList = [False, results, "resultCleaner input was a None value"]
        return rtnList
    import re
    
    listDic = []
    for entry in results:
        data = str(entry[1])
        
        cn = re.findall('\'cn\': \[b\'(.*?)\'\]', data)
        sn = re.findall('\'sn\': \[b\'(.*?)\'\]', data)
        telephoneNumber = re.findall('\'telephoneNumber\': \[b\'(.*?)\'\]', data)
        description = re.findall('\'description\': \[b\'(.*?)\'\]', data)

        if len(cn) == 0:
            cn.append("None")
        if len(sn) == 0:
            sn.append("None")
        if len(telephoneNumber) == 0:
            telephoneNumber.append("None")
        if len(description) == 0:
            description.append("None")

        dict = {
            "cn" : cn[0],
            "sn" : sn[0],
            "tel" : telephoneNumber[0],
            "desc" : description[0]
        }
        listDic.append(dict)
    
    rtnList = [True, listDic]
    print("Cleaned data in dict as list:")
    print(listDic)
    return rtnList