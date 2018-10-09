import re
import BaseHTTPServer
import piinit
import remotekey
import jsonh


HOST = ""
PORT = 80
piDevs = piinit.rcsetup()
server_class = BaseHTTPServer.HTTPServer


class piHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        
        request =  re.compile('/(\w+)/(\w+)/(\w+)')
        matchy = re.match(request, self.path)

        if matchy:
            request_tupel = matchy.groups()
            if request_tupel[0] == "initDev":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(str(remotekey.RDevice.deviceID))
                print("returned DevCounter: " + str(remotekey.RDevice.deviceID))

                return
            elif request_tupel[0] == "initKeys":
                device = piDevs.devices.getDeviceByID(int(request_tupel[1])-1)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(device.actKeys)
                return
            elif request_tupel[0] == "cmd":
                self.send_response(200)
                self.end_headers()

                req_device = piDevs.devices[int(request_tupel[1])]
                req_key    = request_tupel[2]
                req_device.executekey(req_key)
                print("executed " + req_key + ' on ' + req_device.ident)

            elif request_tupel[0] == "getIdent":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(piDevs.devices.getDeviceByID(int(request_tupel[1])-1).ident)
            elif request_tupel[0] == "jsdev":
                self.send_response(200)
                self.end_headers()
                self.wfile.write(jsonh.devList(piDevs.devices))


try:
    server = server_class((HOST, PORT), piHandler)
    print("Server online")
    server.serve_forever()
except KeyboardInterrupt:
    pass
    server.server_close()



