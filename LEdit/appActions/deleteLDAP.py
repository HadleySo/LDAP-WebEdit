import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")

def deleteRequesetFull(request):
    from . import connections

    # Connect and Bind to LDAP server
    conn = connections.connect()
    if conn == None:
        print("[ERROR] Search failed due to failed connection")
        editResult = [False, "[ERROR] Search failed due to failed connection"]
        return editResult
    bindResult = connections.bind(conn)
    if not (bindResult == None):
        connections.disconnect(conn)
        editResult = [False, bindResult]
        return editResult
    
    connections.disconnect(conn)

def resultDNSorter(results):
    print("INFO: Getting full DN from LDAP search results")
    if not isinstance(results, list):
        print("INFO: resultDNSorter input was not a list" + str(type(results)))
        rtnList = [False, results, "resultDNSorter input was not a list" + str(type(results))]
        return rtnList
    if results == None:
        print("INFO: resultDNSorter input was a None value")
        rtnList = [False, results, "resultDNSorter input was a None value"]
        return rtnList
    import re
    
    fullDNlist = []
    for entry in results:
        data = str(entry[0])

        if len(data) == 0:
            data.append("None")

        fullDNlist.append(data)
    
    rtnList = [True, fullDNlist]
    return rtnList