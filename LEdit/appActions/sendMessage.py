import socket
import random
import time
import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")
extentionMap = os.path.normpath((__file__) + "../../../../data/extMap.txt")

# MESSAGE sip:user2@domain.com SIP/2.0
# Via: SIP/2.0/TCP user1pc.domain.com;branch=z9hG4bK776sgdkse
# Max-Forwards: 70
# From: sip:user1@domain.com;tag=49583
# To: sip:user2@domain.com
# Call-ID: asd88asd77a@1.2.3.4
# CSeq: 1 MESSAGE
# Content-Type: text/plain
# Content-Length: 18

# Watson, come here.

def sendTextMessage(request):

    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[ERROR] sendMessge.py - Failed to read config file")
        print(str(e))
        return [False, str(e)]

    DESTINATION_PLAIN = request.form['dest_ext']

    try:
        extMap = configparser.ConfigParser()
        extMap.read(extentionMap)
    except Exception as e:
        print("[ERROR] sendMessge.py - Failed to read extention map file")
        print(str(e))
        return [False, str(e)]

    try:
        DES_EXT = extMap.get(DESTINATION_PLAIN, 'extension')
        DES_IP = extMap.get(DESTINATION_PLAIN, 'ip_address')
        MESSAGE = request.form['message']
    except Exception as e:
        print("[ERROR] sendMessge.py - Failed to get extension IP or number")
        print(str(e))
        return [False, str(e)]

    try:
        R_PORT = cfg.get('SIPTXT', 'port')
        SYS_NAME = cfg.get('SIPTXT', 'systemname')
        SYS_DOMAIN = cfg.get('SIPTXT', 'systemdomain')
    except Exception as e:
        print("[ERROR] sendMessge.py - Failed to get system SIP SMS info")
        print(str(e))
        return [False, str(e)]

    # Line one message
    message = "MESSAGE sip:" 
    message += DES_EXT
    message += "@"
    message += DES_IP
    message += " SIP/2.0"
    message += "\r\n"

    # Line two Via
    message += "Via: SIP/2.0/TCP "
    message += SYS_NAME
    message += ";branch=z9hG4bK" + str(time.time_ns())
    message += "\r\n"

    # Line three Forwards
    message += "Max-Forwards: 70"
    message += "\r\n"

    # Line four From
    message += "From: sip:"
    message += SYS_NAME + "@" + SYS_DOMAIN 
    message += ";tag=" + str(time.time_ns())
    message += "\r\n"

    # Line five To
    message += "To: sip:"
    message += DES_EXT
    message += "@"
    message += DES_IP
    message += "\r\n"

    # Line six Call-ID
    message += "Call-ID:" + str(random.randint(111, 888)) + DES_IP + str(time.time_ns())
    message += "\r\n"

    # Line seven CSeq
    message += "CSeq: "
    message += str(random.randint(11, 95))
    message += " MESSAGE"
    message += "\r\n"

    # Line eight Type
    message += "Content-Type: text/plain"
    message += "\r\n"

    # Line eight Length
    message += "Content-Length: "
    message += str(len(MESSAGE))
    message += "\r\n"

    message += "\r\n"
    message += MESSAGE

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    output = ""

    try:
        output = s.sendto(bytes(message, 'utf-8'), (str(DES_IP), int(R_PORT)))
    except Exception as e:
        print("[ERROR] sendMessge.py - Failed to send message")
        print(str(e))
        return [False, str(e)]
    finally:
        s.close()
    
    return [True, str(output)]

def getExt():
    # Try to read ext map file
    try:
        extMap = configparser.ConfigParser()
        extMap.read(extentionMap)
    except Exception as e:
        print("[ERROR] sendMessge.py - Failed to read extention map file")
        print(str(e))
        return False
    
    # Try to read sections/rooms
    try:
        rooms = extMap.sections()
    except Exception as e:
        print("[ERROR] Failed to read config sections")
        print(str(e))
        return False
    
    return rooms