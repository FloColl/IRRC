from subprocess import call
import clientS
from pixml import buttonxml

xml_buttons = buttonxml()


class remotekey:



    def __init__(self, ident):
        self.permission = 0
        if ident in remotekey.idents:
            self.ident = ident
        else:
            self.ident = "none"
            print('unknown ident ' + ident)

    def getident(self):
        return self.ident
    def setHTML(self, HTMLClass):
        self.HTMLClass = HTMLClass
    def setPermission(self, per):
        self.Permission = per

class irkey(remotekey):

    def __init__(self, remotekey):
        self.ident = remotekey.ident

class netkey(remotekey):

    def __init__(self, ident):
        self.ident = ident


class RDevice:
    deviceID = 0


    def __init__(self):
        self.keys = []
        self.ID = RDevice.deviceID
        RDevice.deviceID = RDevice.deviceID + 1
        self.permission = 0
    def setPermission(self, per):
        self.permission = per
    def setIdent(self, ident):
        self.ident = ident
    def addButton(self, key):
        self.keys.append(key)
    def getCounter(self):
        return RDevice.deviceID + 1

class IRDevice(RDevice):
    print(xml_buttons.getZip())
    irDict = dict(xml_buttons.getZip())

    def __init__(self):
        self.keys = []
        self.ID = RDevice.deviceID
        RDevice.deviceID = RDevice.deviceID + 1

    def setIRID(self, id):
        self.IRID = id

    def executekey(self, ident):
        stringCMD = call(["irsend", "SEND_ONCE", self.IRID, IRDevice.irDict[ident]])


class deviceSet:
    def __init__(self):
        self.deviceDict = {}
    def getDeviceByID(self, devID):
        return self.deviceDict[devID]
    def addDevice(self, device):
        self.deviceDict[device.ID] = device

class NetRDevice(RDevice):

    def __init__(self):
        self.keys = []
        self.idents = self.keys
        self.ID = RDevice.deviceID
        RDevice.deviceID = RDevice.deviceID + 1

    def setAdress(self, addr, port):
        self.adress = (addr, port)

    def executekey(self, req_key):
        clientS.netCmd(self.ident, req_key, self.adress)


