import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")

def editRequesetFull(request):
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
