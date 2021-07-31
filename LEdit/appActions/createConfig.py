import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")

def main(request):
        try:
            cfg = configparser.ConfigParser()

            # modify config
            cfg['LDAP'] = {'ip_address' : request.form['ipAdd'],
                'SearchBaseOne' : request.form['SearchBaseOne'],
                'SearchBaseTwo' : request.form['SearchBaseTwo']}
            cfg['CREDENTIALS'] = {'DN' : request.form['DN'],
                'PW' : request.form['PW']}  

            with open(configPathFull, 'w') as saveConfig:
                cfg.write(saveConfig)                           # save config
            
            return True
        except Exception as e:
            print("[ERROR] failed to create config file")
            print (str(e))
            return False