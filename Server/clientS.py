import socket as s

class netCon:
    def __init__(self, req, addr):
        sock = s.socket(s.AF_INET, s.SOCK_STREAM)
        sock.connect(addr)
        sock.sendall(req.encode("utf-8"))
        self.List = []
        self.finished = 1
        while self.finished:
            msg = sock.recv(4).decode("utf-8")
            if msg:
                self.finished= int(msg[0])
                item = sock.recv(int(msg[1:4])).decode("utf-8")
                self.List.append(item)
        sock.close()
        print("Socket geschlossen ...")



class netCmd:
    def __init__(self, dev, ident, addr):
        sock1 = s.socket(s.AF_INET, s.SOCK_STREAM)
        cmd = ".".join([dev, ident])
        sock1.connect(addr)
        sock1.sendall(cmd.encode("utf-8"))
        print("tried " + ident + " on " + dev)
        sock1.close()





