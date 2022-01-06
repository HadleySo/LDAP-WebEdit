import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")


def main(request):
    try:
        cfg = configparser.ConfigParser()

        # modify config
        cfg['LDAP'] = {'ip_address': request.form['ipAdd'],
                       'SearchBaseOne': request.form['SearchBaseOne'],
                       'SearchBaseTwo': request.form['SearchBaseTwo'],
                       'SearchBaseOne-Name': request.form['SearchBaseOne_Name'],
                       'SearchBaseTwo-Name': request.form['SearchBaseTwo_Name'],
                       'LocalDisplayName': request.form['LocalDisplayName']}
        cfg['CREDENTIALS'] = {'DN': request.form['DN'],
                              'PW': request.form['PW']}
        cfg['LOCAL'] = {'backgroundColor': request.form['backColor'],
                        'LDAP_add_notes': request.form['add_notes']}
        cfg['SIPTXT'] = {'port': request.form['SIPtextPort'],
                            'systemname': request.form['SIPtextSystemName'],
                            'systemdomain' :request.form['SIPtextSystemDomain']}
                            
        with open(configPathFull, 'w') as saveConfig:
            cfg.write(saveConfig)                           # save config

        return True
    except Exception as e:
        print("[ERROR] failed to create config file")
        print(str(e))
        return False


def getConfig():
    print("INFO: Reading config sections. GetConfig as list")
    # Try to read config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[ERROR] Failed to read config file")
        print(str(e))
        return False

    # Try to read sections
    try:
        sections = cfg.sections()
    except Exception as e:
        print("[ERROR] Failed to read config sections")
        print(str(e))
        return False

    outList = []
    for sect in sections:
        outList.append(str(sect))
        for key in cfg[sect]:
            outList.append(str(key) + "  .....  " + str(cfg[sect][key]))
            outList.append("--")

    print(outList)
    return outList


def getConfigDict():
    print("INFO: Reading config sections. GetConfig as dict")
    # Try to read config file
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[ERROR] Failed to read config file")
        print(str(e))
        return None

    # Try to read sections
    try:
        sections = cfg.sections()
    except Exception as e:
        print("[ERROR] Failed to read config sections")
        print(str(e))
        return None

    outDict = {}
    for sect in sections:
        for key in cfg[sect]:
            outDict[str(key)] = str(cfg[sect][key])

    print(str(outDict))
    return outDict
