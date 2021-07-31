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