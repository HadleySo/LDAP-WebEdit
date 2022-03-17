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
    # Get config
    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[ERROR] sendMessage.py - Failed to read config file")
        print(str(e))
        return [False, str(e)]

    # Check if sending to one endpoint or all
    if request.form['send_all'] == "false_send_all":
        print("[INFO] sendMessage.py - sending to one endpoint")

        try:
            DESTINATION_ID = request.form['dest_id']
        except Exception as e:
            print("[ERROR] sendMessage.py - Failed to get destination")
            print(str(e))
            message = "Destination not specified - " + str(e)
            return [False, message]

        return sendMessageHelper(request, DESTINATION_ID)

    elif request.form['send_all'] == "true_send_all":
        print("[INFO] sendMessage.py - sending to all endpoints")

        try:
            extMap = configparser.ConfigParser()
            extMap.read(extentionMap)
        except Exception as e:
            print("[ERROR] sendMessage.py - Failed to read extention map file")
            print(str(e))
            return [False, str(e)]
        
        try:
            rooms = extMap.sections()
        except Exception as e:
            print("[ERROR] sendMessage.py - Failed to read rooms from extention map file")
            print(str(e))
            return [False, str(e)]

        for room in rooms:
            result = sendMessageHelper(request, room)

            if result[0] == False:
                return result
        result[1] = str(result[1]) + " - SENT TO ALL"
        return result

def sendMessageHelper(request, DESTINATION_ID):

    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[ERROR] sendMessage.py - Failed to read config file")
        print(str(e))
        return [False, str(e)]

    try:
        extMap = configparser.ConfigParser()
        extMap.read(extentionMap)
    except Exception as e:
        print("[ERROR] sendMessage.py - Failed to read extention map file")
        print(str(e))
        return [False, str(e)]

    try:
        DES_EXT = extMap.get(DESTINATION_ID, 'extension')
        DES_IP = extMap.get(DESTINATION_ID, 'ip_address')
        MESSAGE = request.form['message']
    except Exception as e:
        print("[ERROR] sendMessage.py - Failed to get extension IP or number")
        print(str(e))
        return [False, str(e)]

    if (len(MESSAGE) > 255):
        return [False, "Message too long!"]
    elif (len(MESSAGE) < 2):
        return [False, "Message too short!"]

    MESSAGE = str(MESSAGE).replace('"', '')

    try:
        R_PORT = cfg.get('SIPTXT', 'port')
        SYS_NAME = cfg.get('SIPTXT', 'systemname')
        SYS_DOMAIN = cfg.get('SIPTXT', 'systemdomain')
    except Exception as e:
        print("[ERROR] sendMessge.py - Failed to get system SIP SMS info")
        print(str(e))
        return [False, str(e)]

    try: 
        SYS_NAME = request.form['systemname']
    except:
        print("[INFO] sendMessage.py - No system name specified in request")
        
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
    
    return_message = str(output) + " - {MGS: " + MESSAGE + "}"
    return [True, str(return_message)]

def getExt():
    # Try to read ext map file
    try:
        extMap = configparser.ConfigParser()
        extMap.read(extentionMap)
    except Exception as e:
        print("[ERROR] sendMessage.py - Failed to read extention map file")
        print(str(e))
        return False
    
    # Try to read sections/rooms
    try:
        rooms = extMap.sections()
        
        roomArray = []                                      # each entry is another array of [id, name] 
        for room in rooms:
            tempArray = ["id", "name"]
            tempArray[0] = room
            tempArray[1] = extMap[room]["name"]
            roomArray.append(tempArray)

    except Exception as e:
        print("[ERROR] sendMessage.py - Failed to read config sections")
        print(str(e))
        return False
    
    return roomArray
