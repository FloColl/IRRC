import xml.etree.ElementTree as ET
from subprocess import call
import vlc

PATH = "devs.xml"

class pyClient:

    devContainer = None

    def __init__(self):
        self.xml = xmlhandler()

    def factory(self, device):
        if device == "radio" : return radio()
        if device == "os" : return osDevice()

    def getKeys(self, dev):
        return self.factory(dev).idents

    def handle(self, request):
        print("try to handle " + request)
        request = request.split(".")
        if len(request) == 1:
            if request[0] == "init": return self.xml.getPyDevs()
            if request[0] in self.xml.getPyDevs(): return self.factory(request[0]).getKeys()
        else:
            if request[0] in self.xml.getPyDevs():
                self.execute(request)
    def getDevices(self):
        return self.xml.getPyDevs()

    def execute(self, cmd):
        dev, key = cmd
        temp = self.factory(dev)
        temp.execcmd(key)

class osDevice:
    def __init__(self):
        self.idents = xmlhandler().getOsCmds()

    def execcmd(self, cmd):
        call(xmlhandler().findOsCmd(cmd))

    def getKeys(self):
        return self.idents

class radio:

    instance =  vlc.Instance("--input-repeat=-1")
    player  = instance.media_player_new()

    def getKeys(self):
        return self.idents

    def __init__(self):
        self.idents=["playarrow", "play/pause", "power", "stop"]

    def __repr__(self):
        return "radio"

    def execcmd(self, cmd):

        if cmd == "power":
            sender = radio.instance.media_new(xmlhandler().findRadioCmds("arrow"))
            pyClient.devContainer = radio.player
            pyClient.devContainer.set_media(sender)
            pyClient.devContainer.play()
        if cmd == "stop":
            pyClient.devContainer.stop()
        if cmd == "play":
            pyClient.devContainer.play()



class xmlhandler:

    def __init__(self):
        self.root = ET.parse(PATH).getroot()

    def getPyDevs(self):
        return [dev.tag for dev in self.root.find("scriptcmds")]+["os"]

    def getOsCmds(self):
        return [cmd.tag for cmd in self.root.find("oscmds")]

    def findOsCmd(self, ident):
        return self.root.find("oscmds").find(ident).text

    def findRadioCmds(self, ident):
        return self.root.find("scriptcmds").find("radio").find(ident).text

    def getKeys(self, dev):
        print("get keylist from: " + dev)
        return [key.tag for key in self.root.find("scriptcmds").find(dev)]


