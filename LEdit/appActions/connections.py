import configparser
import os
import ldap

configPathFull = os.path.normpath((__file__) + "../../data/config.txt")

# Create base connection to LDAP server.
# Not authenticated yet
def connect():
    # Get LDAP server address from config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
        ipAdd = cfg.get('LDAP','ip_address').strip()
    except:
        print("[ERROR] Unable to open config file to get ip address")
        return None

    # Connect to LDAP server
    try:
        conn = ldap.initialize('ldap://' + ipAdd)
        return conn
    except ldap.LDAPError as e:
        print("[ERROR] Unable to CONNECT to LDAP server")

        print (e.message['info'])   
        if type(e.message) == dict and e.message.has_key('desc'):
            print (e.message['desc'])   
        else:
            print (e)
        return None

# After conenction to LDAP server.
# Authenticates with DN and PW
def bind(conn):
    # Get LDAP server address from config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
        DN = cfg.get('CREDENTIALS','DN').strip()
        PW = cfg.get('CREDENTIALS','PW')
    except:
        print("[ERROR] Unable to open config file to get DN and PW")
        return None

    # Bind with DN and Password
    try:
        conn.bind(DN, PW, ldap.AUTH_SIMPLE)
        return True
    except ldap.LDAPError as e:
        print("[ERROR] Unable to BIND to LDAP server")

        print (e.message['info'])   
        if type(e.message) == dict and e.message.has_key('desc'):
            print (e.message['desc'])   
        else:
            print (e)
        return None