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
    
    dn = ""
    attr_name = ""
    attr_val = request.form['searchString']
    searchFilter = '(objectclass=person)'

    # Set attributes based on form
    if request.form['searchBase'] == 'baseOne':
        dn = cfg.get('LDAP','searchbaseone').strip()
    elif request.form['searchBase'] == 'baseTwo':
        dn = cfg.get('LDAP','searchbasetwo').strip()

    if request.form['searchField'] == 'notes':
        attr_name = ['description']
    elif request.form['searchField'] == 'pNum':
        attr_name = ['telephoneNumber']
    elif request.form['searchField'] == 'lName':
        attr_name = ['sn']
    elif request.form['searchField'] == 'fName':
        attr_name = ['cn']

    # Execute search
    try:
        import ldap
        successResults = conn.search_s( dn, ldap.SCOPE_SUBTREE, searchFilter, attr_name )
        querryResult = [True, successResults]
        connections.disconnect(conn)
        return querryResult
    except Exception as e:
        connections.disconnect(conn)
        print("[ERROR] Unable to complete search.")
        querryResult = [False, "[ERROR] Unable to complete search. " + str(e)]
        return querryResult

    # Close connection when done
    connections.disconnect(conn)

    querryResult = [False, "[ERROR] Unable to complete search. Unknown reason"]
    return querryResult