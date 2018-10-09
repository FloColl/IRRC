import re
import clientS
import pixml
import remotekey
import socket

PATH = "CT-865"
NETPATH = "netdevices.xml"

class rcsetup:
    buxml = pixml.buttonxml()
    riDict = dict(buxml.getAZip())
    def initirdevs(self, path):
        config = open(path, 'r')
        print('Load IR-Config file ' + path)
        remotematch = re.compile('begin remote')
        codematch   = re.compile('begin codes')
        codematchend= re.compile('end codes')
        buttonmatch = re.compile('[ ]+([_\w]+)')
        namematch   = re.compile('name[ ]+([-_\S]+)')
        identmatch  = re.compile('#ident[ ]+(\w+)')


        for line in config:
            if remotematch.search(line):
                device = remotekey.IRDevice()
                name = ""
                for line in config:
                    tempname = namematch.search(line)
                    if tempname:
                        name = tempname.group(1)
                        device.setIRID(name)
                        break
                for line in config:
                    tempident = identmatch.search(line)
                    if tempident:
                        ident = tempident.group(1)
                        device.setIdent(ident)
                        break
                    else:
                        device.setIdent(name)
                        break

                for line in config:
                    added = False
                    if codematch.search(line):
                        for line in config:
                            temp = buttonmatch.match(line)
                            if codematchend.search(line):
                                self.devices.append(device)
                                added = True
                                print('Device ' + device.ident + ' added' + ' with ID ' + str(device.ID))
                                break

                            try:
                                rcsetup.riDict[temp.group(1)]
                            except KeyError:
                                print("No ident Found for " + temp.group(1) + "! Enter ident")
                                tempin = str(raw_input())
                                remotekey.IRDevice.irDict[temp.group(1)]=tempin
                                rcsetup.riDict[temp.group(1)] = tempin
                                rcsetup.buxml.addButton(tempin, temp.group(1))
                            finally:
                                device.keys.append(rcsetup.riDict[temp.group(1)])



                    if added:
                        break

    def __init__(self):
        self.devices = []
        self.initirdevs(PATH)
        self.initnetdevs(NETPATH)

    def initnetdevs(self, path):
        for dev in pixml.piNetXml(path).List:
            try:
                temp = remotekey.NetRDevice()
                temp.setAdress(dev[1]["host"], int(dev[1]["port"]))
                temp.setIdent(dev[0])
                temp.keys = self.getNetKeys(temp)
                temp.actKeys = temp.keys
                self.devices.append(temp)
                print("Device " + temp.ident)
            except socket.error:
                print("failed to connect to " + dev[0])


    def getNetKeys(self, device):

        return clientS.netCon(device.ident, device.adress).List















