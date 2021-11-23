import socket
import random
import time
import configparser
import os

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")

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

def sendTextMessage(DES_EXT, DES_IP, MESSAGE):

    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
    except Exception as e:
        print("[ERROR] sendMessge.py - Failed to read config file")
        print(str(e))
        return False

    R_PORT = cfg.get('SIPTXT', 'port')
    SYS_NAME = cfg.get('SIPTXT', 'systemname')
    SYS_DOMAIN = cfg.get('SIPTXT', 'systemdomain')

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
    message += len(MESSAGE)
    message += "\r\n"

    message += "\r\n"
    message += MESSAGE

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.sendto(bytes(message, 'utf-8'), (str(DES_IP), int(R_PORT)))
    except socket.error:
        pass
    finally:
        s.close()

