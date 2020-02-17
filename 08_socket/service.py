import socket
import struct
import os
import subprocess
import socketserver
import time
import hashlib
import pickle


dataFormat = '8s32s100s100sl'
os.chdir(os.path.abspath(os.path.dirname(__file__)))
usePickle = False


class fileServer(socketserver.StreamRequestHandler):
    def struct_pack(self):
        ret = b''
        if usePickle is True:
            tmp = [self.action, self.md5sum, self.clientfilePath,
                   self.serverfilePath, self.size]
            print(tmp)
            ret = pickle.dumps(tmp)
        else:
            ret = struct.pack(dataFormat, self.action.encode(), self.md5sum.encode(), self.clientfilePath.encode(),
                              self.serverfilePath.encode(), self.size)

        return ret

    def struct_unpack(self, package):
        self.action, self.md5sum, self.clientfilePath, self.serverfilePath, self.size = struct.unpack(dataFormat,
                                                                                                      package)
        self.action = self.action.decode().strip('\x00')
        self.md5sum = self.md5sum.decode().strip('\x00')
        self.clientfilePath = self.clientfilePath.decode().strip('\x00')
        self.serverfilePath = self.serverfilePath.decode().strip('\x00')

    def handle(self):
        print('connected from:', self.client_address)
        fileinfo_size = struct.calcsize(dataFormat)
        self.buf = self.request.recv(fileinfo_size)
        if self.buf:
            self.struct_unpack(self.buf)
            print("get action: "+self.action)
            if self.action.startswith("upload"):
                try:
                    if os.path.isdir(self.serverfilePath):
                        fileName = (os.path.split(self.clientfilePath))[1]
                        self.serverfilePath = os.path.join(
                            self.serverfilePath, fileName)
                    filePath, fileName = os.path.split(self.serverfilePath)
                    if not os.path.exists(filePath):
                        self.request.send(str.encode('dirNotExist'))
                    else:
                        self.request.send(str.encode('ok'))
                        recvd_size = 0
                        file = open(self.serverfilePath, 'wb')
                        while not recvd_size == self.size:
                            if self.size - recvd_size > 1024:
                                rdata = self.request.recv(1024)
                                recvd_size += len(rdata)
                            else:
                                rdata = self.request.recv(
                                    self.size - recvd_size)
                                recvd_size = self.size
                            file.write(rdata)
                        file.close()
                        (status, output) = subprocess.getstatusoutput(
                            "md5sum " + self.serverfilePath + " | awk '{printf $1}'")
                        if output == self.md5sum:
                            self.request.send(str.encode('ok'))
                        else:
                            self.request.send(str.encode('md5sum error'))
                except Exception as e:
                    print(e)
                finally:
                    self.request.close()
            elif self.action.startswith("download"):
                try:
                    if os.path.exists(self.serverfilePath):
                        fo = open(self.serverfilePath, 'rb')
                        # md5 = hashlib.md5()
                        # md5.update(fo.read())
                        # self.md5sum = md5.hexdigest()
                        self.action = 'ok'
                        self.size = os.stat(self.serverfilePath).st_size
                        ret = self.struct_pack()
                        self.request.send(ret)
                        while True:
                            filedata = fo.read(1024)
                            if not filedata:
                                break
                            self.request.send(filedata)
                        fo.close()
                    else:
                        self.action = 'nofile'
                        ret = self.struct_pack()
                        self.request.send(ret)
                except Exception as e:
                    print(e)
                finally:
                    self.request.close()
            elif self.action.startswith("auto"):
                print('send all files to client')
                try:
                    for parent, folders, files in os.walk(os.getcwd()):
                        for folder in folders:
                            self.action = 'path'
                            self.serverfilePath = os.path.join(
                                parent.replace(os.getcwd(), ''), folder)
                            if self.serverfilePath.startswith('\\'):
                                self.serverfilePath = self.serverfilePath[1:]
                            self.size = 0
                            ret = self.struct_pack()
                            self.request.send(ret)
                            time.sleep(0.001)
                        for filename in files:
                            self.action = 'file'
                            self.serverfilePath = os.path.join(
                                parent.replace(os.getcwd(), ''), filename)
                            if self.serverfilePath.startswith('\\'):
                                self.serverfilePath = self.serverfilePath[1:]
                            fo = open(os.path.join(parent, filename), 'rb')
                            # md5 = hashlib.md5()
                            # md5.update(fo.read())
                            self.md5sum = 'TEST'
                            self.size = os.stat(
                                os.path.join(parent, filename)).st_size
                            ret = self.struct_pack()
                            self.request.send(ret)
                            print('sending: ' + filename + ' with size: ' +
                                  str(self.size) + ' and md5: ' + self.md5sum)
                            while True:
                                filedata = fo.read(1024)
                                if not filedata:
                                    break
                                self.request.send(filedata)
                            fo.close()
                            time.sleep(0.001)
                    print('finsh!')
                    self.action = 'finish'
                    ret = self.struct_pack()
                    self.request.send(ret)
                    exit()
                except Exception as e:
                    print(e)
                finally:
                    self.request.close()


if __name__ == "__main__":
    import threading

    myname = socket.getfqdn(socket.gethostname())
    # 获取本机ip
    serverIp = socket.gethostbyname(myname)
    serverPort = 6969
    serverAddr = (serverIp, serverPort)

    class fileServerth(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.create_time = time.time()
            self.local = threading.local()

        def run(self):
            print("fileServer is running at {0} on port {1}".format(
                serverIp, serverPort))
            fileserver.serve_forever()

    fileserver = socketserver.ThreadingTCPServer(
        serverAddr, fileServer)
    fileserverth = fileServerth()
    fileserverth.start()
