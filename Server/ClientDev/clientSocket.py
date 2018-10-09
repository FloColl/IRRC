import socket
import selectors2 as selectors
import custClient

HOST = ""
PORT = 1337

class clientListener:

    identDict = {}
    listenerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    mainSelector = selectors.DefaultSelector()

    def __init__(self):
        self.actClient = custClient.pyClient()
        clientListener.listenerSocket.bind((HOST, PORT))
        clientListener.listenerSocket.listen(6)
        clientListener.listenerSocket.setblocking(False)
        clientListener.mainSelector.register(clientListener.listenerSocket, selectors.EVENT_READ, data=None)

        while True:
            events = clientListener.mainSelector.select(timeout=None)
            for key, mask in events:
                if not key.data:
                    self.accept(key.fileobj)
                else:
                    if not key.data.handled: self.answer(key, mask)
                    clientListener.mainSelector.unregister(key.fileobj)
                    key.fileobj.close()
                    print("closed")


    def accept(self, sock):
        conn, addr = sock.accept()
        print("verbindung akzeptiert von: " )
        conn.setblocking(False)
        print(addr)
        d = reqData(addr, "")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        clientListener.mainSelector.register(conn, events, data=d)

    def answer(self, key, mask):
        sock = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            piRequest = sock.recv(1024).decode("utf-8")
            if not data.handled:
                data.piReq = piRequest
                data.handled = True
            else:
                clientListener.mainSelector.unregister(sock)
                print("closing socket ...")
                sock.close()


        if mask & selectors.EVENT_WRITE:
                handle = self.actClient.handle(data.piReq)
                if handle:
                    answer = handle
                    if isinstance(answer, str):
                        msgLen = "{:04d}".format(len(answer))
                        finmsg = str(msgLen) + answer
                        sock.sendall(finmsg.encode("utf-8"))
                    else:
                        listLen = len(answer)

                        for msg in answer:
                            listLen = listLen-1
                            msgLen = "{:04d}".format(int(min(listLen,1)*1000 + len(msg)))
                            finmsg = str(msgLen)+ msg
                            sock.sendall(finmsg.encode("utf-8"))

class reqData:
    def __init__(self, addr, req):
        self.addr = addr
        self.piReq = req
        self.len = len(req)
        self.handled = False

c = clientListener()

