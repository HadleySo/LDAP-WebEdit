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


def getAll():
    print("INFO: Getting all custom localizaion options")

    name = getName()
    color = getColorBack()

    localOpt = {
        "name": name,
        "color": color
    }
    return localOpt
