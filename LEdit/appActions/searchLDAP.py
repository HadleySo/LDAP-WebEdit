import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")

def getBaseName():
    print("INFO: Trying to get SearchBase names")
    names = []
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[ERROR] Failed to read config file")
        print(str(e))
        return False

    try:
        names.append(cfg.get('LDAP','searchbaseone-name'))
    except Exception as e:
        names.append("")
        print("[WARNING] Failed to read Base ONE Name from config file")
        print(str(e))
    try:
        names.append(cfg.get('LDAP','searchbasetwo-name'))
        return names
    except Exception as e:
        names.append("")
        print("[WARNING] Failed to read Base TWO Name from config file")
        print(str(e))
    return names

def getBaseDN():
    print("INFO: Trying to get Base DN")
    baseDN = []
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[ERROR] Failed to read config file")
        print(str(e))
        return False

    try:
        baseDN.append(cfg.get('LDAP','searchbaseone'))
    except Exception as e:
        baseDN.append(False)
        print("[WARNING] Failed to read Base DN ONE from config file")
        print(str(e))
    try:
        baseDN.append(cfg.get('LDAP','searchbasetwo'))
    except Exception as e:
        baseDN.append(False)
        print("[WARNING] Failed to read Base DN TWO from config file")
        print(str(e))

    return baseDN
        
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
        dn = getBaseDN()[0]
    elif request.form['searchBase'] == 'baseTwo':
        dn = getBaseDN()[1]
    if dn == False:                                                 # When the DN selected does not exist tell user
        print("[ERROR] The Search Base DN you selected is not configured.")
        querryResult = [False, "[ERROR] The Search Base DN you selected is not configured."]
        connections.disconnect(conn)
        return querryResult

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