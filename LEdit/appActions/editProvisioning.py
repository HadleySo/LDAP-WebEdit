import os, configparser
import xml.etree.ElementTree as ET

configPathFull = os.path.normpath((__file__) + "../../../../data/config.txt")


def main(line: int, info: dict):

    try:
        cfg = configparser.ConfigParser()
        cfg.read(configPathFull)
        file_path = cfg.get('PROVISIONING', 'file').strip()
    except Exception as e:
        print("[ERROR] Unable to open config file to get provisioning file")
        print(str(e))
        return None

    if line == "05":
        return modify_5(file_path, info)

    elif line == "06":
        return modify_6(file_path, info)

    elif line == "07":
        return modify_6(file_path, info)

    elif line == "08":
        return modify_6(file_path, info)


def modify_5(file_path: str, info: dict):
    dom1 = ET.parse(file_path)
    line_display = dom1.find("Short_Name_5_")
    line_function = dom1.find("Extended_Function_5_")

    line_display.text = info['display']
    line_function.text = "fnc=sd;ext=9" + info['phone'] + "@192.168.2.5;vid=2;nme=" + info['display']
    
    dom1.write(file_path)
    
def modify_6(file_path: str, info: dict):
    dom1 = ET.parse(file_path)
    line_display = dom1.find("Short_Name_6_")
    line_function = dom1.find("Extended_Function_6_")

    line_display.text = info['display']
    line_function.text = "fnc=sd;ext=9" + info['phone'] + "@192.168.2.5;vid=2;nme=" + info['display'] 

    dom1.write(file_path)

def modify_7(file_path: str, info: dict):
    dom1 = ET.parse(file_path)
    line_display = dom1.find("Short_Name_7_")
    line_function = dom1.find("Extended_Function_7_")
    
    line_display.text = info['display']
    line_function.text = "fnc=sd;ext=9" + info['phone'] + "@192.168.2.5;vid=2;nme=" + info['display']

    dom1.write(file_path)

def modify_8(file_path: str, info: dict):
    dom1 = ET.parse(file_path)
    line_display = dom1.find("Short_Name_8_")
    line_function = dom1.find("Extended_Function_8_")
    
    line_display.text = info['display']
    line_function.text = "fnc=sd;ext=9" + info['phone'] + "@192.168.2.5;vid=2;nme=" + info['display']

    dom1.write(file_path)