import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")

def getName():
    print("INFO: Reading custom name from config")
    # Try to read config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[WARNING] Failed to read config file")
        print(str(e))
        return None
    
    # Try to read sections
    try:
        localName = cfg.get('LDAP','localdisplayname')
        if len(localName) < 1:
            return None
        return localName
    except Exception as e:
        print("[WARNING] Failed to read custom display name")
        print(str(e))
        return None