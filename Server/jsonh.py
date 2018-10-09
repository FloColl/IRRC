import json

def dev2jdict(device):
    jdict = {}
    jdict["ID"]=device.ID
    jdict["ident"]=device.ident
    jdict["Keys"]=device.keys
    return jdict

def devList(devices):
    return json.dumps([dev2jdict(device) for device in devices])
