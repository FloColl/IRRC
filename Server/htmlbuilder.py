import xml.etree.ElementTree as ET

class htmlbuilder:
    def __init__(self):
        self.html = open("index.htm", 'w')
        self.devs = ET.parse("devices.xml")
        self.devroot = self.devs.getroot()
        wpreface()
        wheader()
        wbody()
        wnav()

    def wpreface(self):
        self.html.write("""
        <!DOCTYPE html> \n <html lang="de"> \n
        """)
    def wheader(self):
        head = ET.Element("head")
        title = ET.SubElement(head, "title")
        title.text = "Raspberry GUI"
        sheet = ET.SubElement(head, "link")
        sheet.set("rel", "stylesheet")
        sheet.set("type", "text/css")
        sheet.set("href", "start.css")
    def wbody(self):
        body = ET.Element("body")
        self.maingrid = ET.SubElement(self.body, "div")
        maingrid.set("class", "maingrid")
        headline1 = ET.SubElement(maingrid, "h1")
        headline1.set("class", "headline")
        headline1.text = "Willkommen auf der Startseite des Raspberry!"
        


    def wnav(self):
        self.navigation = ET.SubElement(self.maingrid, "ul")
        self.navigation.set("class", "gridnav")
        for kinds in devroot:
            kind = ET.SubElement(self.navigation, "li")
            kind.text = kinds.tag
            for dev in kinds:
               temp =  ET.SubElement(self.navigation, "li")
               temp.text = dev.tag              
        

    def wdev(self, devgridid, devtree):
        devgrid = ET.Element("div")
        devgrid.set("id", devgridid)


    def getdevtree(self, devint):
        for kinds in self.devroot:
            
