import configparser, os

logMap = os.path.normpath((__file__) + "../../../../data/log-extMap.txt")

def getCalls(request):
    import requests, configparser, bs4
    
    try:
        DESTINATION_ID = request
    except Exception as e:
        print("[ERROR] phoneLog.py - Failed to get DESTINATION_ID from request")
        print(str(e))
        return [False, str(e)]

    try:
        extMap = configparser.ConfigParser()
        extMap.read(logMap)
    except Exception as e:
        print("[ERROR] phoneLog.py - Failed to read extention map file")
        print(str(e))
        return [False, str(e)]

    try:
        DES_IP = extMap.get(DESTINATION_ID, 'ip_address')
    except Exception as e:
        print("[ERROR] phoneLog.py - Failed to get extension IP or number")
        print(str(e))
        return [False, str(e)]


    try:
        destURL = 'http://' + DES_IP + '/calllog.htm'
        response = requests.get(destURL, timeout=5)

        soup = bs4.BeautifulSoup(response.content)
        page_missed = soup.find("div", {"id": "Missed"})
        page_placed = soup.find("div", {"id": "Placed"})
        page_answered = soup.find("div", {"id": "Answered"})

        full_page = """
        <html> 
        <head>
          <style type="text/css">
            p.p1 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Times; color: #000000; -webkit-text-stroke: #000000; min-height: 14.0px}
            p.p2 {margin: 0.0px 0.0px 0.0px 0.0px; font: 12.0px Times; color: #000000; -webkit-text-stroke: #000000}
            span.s1 {font-kerning: none}
            table.t1 {width: 784.0px}
            td.td1 {width: 15.0px; background-color: #e3ecf6; padding: 1.0px 1.0px 1.0px 1.0px}
            td.td2 {width: 372.9px; background-color: #e3ecf6; padding: 1.0px 1.0px 1.0px 1.0px}
            td.td3 {width: 373.2px; background-color: #e3ecf6; padding: 1.0px 1.0px 1.0px 1.0px}
            td.td4 {width: 15.0px; background-color: #f1faff; padding: 1.0px 1.0px 1.0px 1.0px}
            td.td5 {width: 372.9px; background-color: #f1faff; padding: 1.0px 1.0px 1.0px 1.0px}
            td.td6 {width: 373.2px; background-color: #f1faff; padding: 1.0px 1.0px 1.0px 1.0px}
        </style>
        <title>Call Log</title>
        </head>
        <body>
        <h1> MISSED </h1>
        """
        
        full_page += page_missed.prettify() + "<h1> PLACED </h1>" + page_placed.prettify() + "<h1> ANSWERED </h1>" + page_answered.prettify()

        return [True, response, full_page]
    except Exception as e:
        print("[ERROR] phoneLog.py - Failed to get log webpage")
        return [False, str(e)]

def getExt():
    # Try to read ext map file
    try:
        extMap = configparser.ConfigParser()
        extMap.read(logMap)
    except Exception as e:
        print("[ERROR] phoneLog.py - Failed to read extention map file")
        print(str(e))
        return False
    
    # Try to read sections/rooms
    try:
        rooms = extMap.sections()
        
        roomArray = []                                      # each entry is another array of [id, name] 
        for room in rooms:
            tempArray = ["id", "name"]
            tempArray[0] = room
            tempArray[1] = extMap.get(room, "name")
            roomArray.append(tempArray)

    except Exception as e:
        print("[ERROR] phoneLog.py - Failed to read config sections")
        print(str(e))
        return False
    
    return roomArray
