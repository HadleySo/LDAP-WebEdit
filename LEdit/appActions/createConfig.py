import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")

def main(request):
        try:
            cfg = configparser.ConfigParser()

            # modify config
            cfg['LDAP'] = {'ip_address' : request.form['ipAdd'],
                'SearchBaseOne' : request.form['SearchBaseOne'],
                'SearchBaseTwo' : request.form['SearchBaseTwo'],
                'SearchBaseOne-Name' : request.form['SearchBaseOne_Name'],
                'SearchBaseTwo-Name' : request.form['SearchBaseTwo_Name'],
                'LocalDisplayName' : request.form['LocalDisplayName']}
            cfg['CREDENTIALS'] = {'DN' : request.form['DN'],
                'PW' : request.form['PW']}  
            cfg['LOCAL'] = {'backgroundColor' : request.form['backColor']}

            with open(configPathFull, 'w') as saveConfig:
                cfg.write(saveConfig)                           # save config
            
            return True
        except Exception as e:
            print("[ERROR] failed to create config file")
            print (str(e))
            return False

def getConfig():
    print("INFO: Reading config sections")
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