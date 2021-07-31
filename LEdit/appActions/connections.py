import configparser
import os
import ldap

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")

# Create base connection to LDAP server.
# Not authenticated yet
def connect():
    # Get LDAP server address from config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
        ipAdd = cfg.get('LDAP','ip_address').strip()
    except Exception as e:
        print("[ERROR] Unable to open config file to get ip address")
        print(str(e))
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
# Return Nothing if ok. Otherwise return error message
def bind(conn):
    # Get LDAP server address from config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
        DN = cfg.get('CREDENTIALS','DN').strip()
        PW = cfg.get('CREDENTIALS','PW')
    except Exception as e:
        print("[ERROR] Unable to open config file to get DN and PW")
        print(str(e))
        return "[ERROR] Unable to open config file to get DN and PW"

    # Bind with DN and Password
    try:
        conn.bind(DN, PW, ldap.AUTH_SIMPLE)
        return None
    except ldap.INVALID_CREDENTIALS:
        print ("Your username or password is incorrect.")
        return "[ERROR] Your username or password is incorrect"
    except ldap.LDAPError as e:
        print("[ERROR] Unable to BIND to LDAP server")
        print (str(e))
        return "[ERROR] Unable to BIND to LDAP server" + (str(e))
    except Exception as e:
        print("[ERROR] Unable to BIND to LDAP server")
        print(str(e))
        return "[ERROR] Unable to BIND to LDAP server" + (str(e))

def disconnect(conn):
    try:
        conn.unbind()
        return None
    except Exception as e:
        print("[ERROR] Unable to UNBIND")
        print(str(e))
        return "[ERROR] Unable to UNBIND " + (str(e))