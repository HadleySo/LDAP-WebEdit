import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")


def getName():
    genericName = ""
    print("INFO: Reading custom name from config")
    # Try to read config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[WARNING] Failed to read config file")
        print(str(e))
        return genericName

    # Try to read sections
    try:
        localName = cfg.get('LDAP', 'localdisplayname')
        if len(localName) < 1:
            return genericName
        return localName
    except Exception as e:
        print("[WARNING] Failed to read custom display name")
        print(str(e))
        return genericName


def getColorBack():
    print("INFO: Reading custom color from config")

    genericColor = "#000000"

    # Try to read config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[WARNING] Failed to read config file")
        print(str(e))
        return genericColor

    # Try to read sections
    try:
        custColor = cfg.get('LOCAL', 'backgroundColor')
        return custColor
    except Exception as e:
        print("[WARNING] Failed to read custom color")
        print(str(e))
        return genericColor
 
def getAddNotes():
    print("INFO: Reading LDAP add notes from config")

    # Try to read config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[WARNING] Failed to read config file")
        print(str(e))
        return ""

    # Try to read sections
    try:
        notes = cfg.get('LOCAL', 'LDAP_add_notes')
        return notes
    except Exception as e:
        print("[WARNING] Failed to read LDAP add notes")
        print(str(e))
        return ""

def getAll():
    print("INFO: Getting all custom localization options")

    name = getName()
    color = getColorBack()
    adding_notes = getAddNotes()

    localOpt = {
        "name": name,
        "color": color,
        "addNotes": adding_notes
    }
    return localOpt
