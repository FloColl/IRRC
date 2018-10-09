import xml.etree.ElementTree as ET

class xmlbuilder:
    devices_xml = "devices.xml"
    buttons_xml = "key.xml"

    def inittree(self, htmlfile):
        self.root = ET.Element("Devices")
        self.IRdevs = ET.SubElement(self.root, "IR-Devices")
        self.devs = ET.SubElement(self.root, "Net-Devices")


    def __init__(self):
        self.fhtml = open(devices_xml, 'w')
        self.inittree(self.fhtml)

    def getTree(self):
        return self.tree

    def addIRDev(self, irdevice):
        newDevice = ET.SubElement(self.IRdevs, irdevice.ident)

        newDevice.set('Dev.NR', str(irdevice.devInt))
        newDevice.set('name', irdevice.name)

        newDeviceKeys = ET.SubElement(newDevice, 'Keys')

        for key in irdevice.keys:
            newKey = ET.SubElement(newDeviceKeys, key)

    def xmlwrite(self):
        self.tree = ET.ElementTree(self.root)
        self.tree.write(self.fhtml)


class buttonxml:
    def __init__(self):
        self.buttons = ET.parse("key.xml")
        self.rootbutton = self.buttons.getroot()

    def addButton(self, key, ident):
        a = ET.SubElement(self.rootbutton, ident)
        a.text = key
        self.buttons.write("key.xml")

    def getKey(self, ident):
        return self.rootbutton.find(ident).text

    def getZip(self):
        return [(button.text, button.tag) for button in self.rootbutton]

    def getAZip(self):
        return [(button.tag, button.text) for button in self.rootbutton]




class piNetXml:
    def __init__(self, path):
        xml = ET.parse(path)
        root = xml.getroot()
        self.List = []
        for netDevice in root:
            self.List.append((netDevice.tag, netDevice.attrib))



