import socket
import struct
import os
import subprocess
import shutil
import time
import hashlib
import pickle


serverIp = '192.168.0.9'
serverPort = 6969
usePickle = False
dataFormat = '8s32s100s100sl'
os.chdir(os.path.abspath(os.path.dirname(__file__)))


class fileClient():
    def __init__(self, addr):
        self.addr = addr
        self.action = ''
        self.fileName = ''
        self.md5sum = ''
        self.clientfilePath = ''
        self.serverfilePath = ''
        self.size = 0

    def struct_pack(self):
        ret = struct.pack(dataFormat, self.action.encode(), self.md5sum.encode(), self.clientfilePath.encode(),
                          self.serverfilePath.encode(), self.size)
        return ret

    def struct_unpack(self, package):
        if usePickle is False:
            self.action, self.md5sum, self.clientfilePath, self.serverfilePath, self.size = struct.unpack(
                dataFormat, package)
            self.action = self.action.decode().strip('\x00')
            self.md5sum = self.md5sum.decode().strip('\x00')
            self.clientfilePath = self.clientfilePath.decode().strip('\x00')
            self.serverfilePath = self.serverfilePath.decode().strip('\x00')
        else:
            self.action, self.md5sum, self.clientfilePath, self.serverfilePath, tempSize = pickle.loads(
                package)
            self.size = int(tempSize)
            print(self.action, self.serverfilePath)

    def sendFile(self, clientfile, serverfile):
        if not os.path.exists(clientfile):
            print('源文件/文件夹不存在')
            return "No such file or directory"
        self.action = 'upload'
        fo = open(clientfile, 'rb')
        md5 = hashlib.md5()
        md5.update(fo.read())
        self.md5sum = md5.hexdigest()
        self.size = os.stat(clientfile).st_size
        self.serverfilePath = serverfile
        self.clientfilePath = clientfile
        ret = self.struct_pack()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(self.addr)
            s.send(ret)
            recv = s.recv(1024)
            if recv.decode() == 'dirNotExist':
                print("目标文件/文件夹不存在")
                return "No such file or directory"
            elif recv.decode() == 'ok':
                fo = open(clientfile, 'rb')
                while True:
                    filedata = fo.read(1024)
                    if not filedata:
                        break
                    s.send(filedata)
                fo.close()
                recv = s.recv(1024)
                if recv.decode() == 'ok':
                    print("文件传输成功")
                    s.close()
                    return 0
                else:
                    s.close()
                    return "md5sum error:md5sum is not correct!"
        except Exception as e:
            print(e)
            return "error:"+str(e)

    def recvFile(self, clientfile, serverfile):
        if not os.path.isdir(clientfile):
            filePath, fileName = os.path.split(clientfile)
        else:
            filePath = clientfile
        if not os.path.exists(filePath):
            print('本地目标文件/文件夹不存在')
            return "No such file or directory"
        self.action = 'download'
        self.clientfilePath = clientfile
        self.serverfilePath = serverfile
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(self.addr)
            ret = self.struct_pack()
            s.send(ret)
            recv = s.recv(struct.calcsize(dataFormat))
            self.struct_unpack(recv)
            if self.action.startswith("ok"):
                if os.path.isdir(clientfile):
                    fileName = (os.path.split(serverfile))[1]
                    clientfile = os.path.join(clientfile, fileName)
                self.recvd_size = 0
                file = open(clientfile, 'wb')
                while not self.recvd_size == self.size:
                    if self.size - self.recvd_size > 1024:
                        rdata = s.recv(1024)
                        self.recvd_size += len(rdata)
                    else:
                        rdata = s.recv(self.size - self.recvd_size)
                        self.recvd_size = self.size
                    file.write(rdata)
                file.close()
                print('\n等待校验...')
                fo = open(clientfile, 'rb')
                md5 = hashlib.md5()
                md5.update(fo.read())
                output = md5.hexdigest()
                fo.close()
                if output == self.md5sum:
                    print("文件传输成功")
                else:
                    print("文件校验不通过")
                    (status, output) = subprocess.getstatusoutput(
                        "rm " + clientfile)
            elif self.action.startswith("nofile"):
                print('远程源文件/文件夹不存在')
                return "No such file or directory"
        except Exception as e:
            print(e)
            return "error:"+str(e)

    def requestAllFile(self):
        if os.path.exists('code'):
            shutil.rmtree('code', ignore_errors=True)
        time.sleep(0.5)
        # try:
        if not os.path.exists('code'):
            os.mkdir('code')
        self.action = 'auto'
        self.clientfilePath = 'code'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.addr)
        ret = self.struct_pack()
        s.send(ret)
        okret = True
        subpath = ''
        while okret:
            if usePickle is False:
                recv = s.recv(struct.calcsize(dataFormat))
            else:
                recv = s.recv(1024*5)
            self.struct_unpack(recv)
            if self.action.startswith("path"):
                subpath = os.path.join('code', self.serverfilePath)
                os.makedirs(subpath, exist_ok=True)
                print('make dir: ' + subpath)
                self.recvd_size = 0
            if self.action.startswith("file"):
                self.recvd_size = 0
                filename = os.path.join('code', self.serverfilePath)
                newfile = open(filename, 'wb')
                while not self.recvd_size == self.size:
                    if self.size - self.recvd_size > 1024:
                        rdata = s.recv(1024)
                        self.recvd_size += len(rdata)
                    else:
                        rdata = s.recv(self.size - self.recvd_size)
                        self.recvd_size = self.size
                    newfile.write(rdata)
                newfile.close()
                print(self.serverfilePath + " 文件传输成功, size: " + str(self.size))
                # fo = open(filename, 'rb')
                # md5 = hashlib.md5()
                # md5.update(fo.read())
                # output = md5.hexdigest()
                # fo.close()
                # if output == self.md5sum:
                #     print(self.serverfilePath +
                #           " 文件传输成功, size: " + str(self.size))
                # else:
                #     print(self.serverfilePath +
                #           " 文件校验不通过, real md5sum: " + str(self.md5sum) + ' , md5sum: ' + str(output))
            elif self.action.startswith("finish"):
                okret = False
        s.close()
        # except Exception as e:
        #     print('Auto: ' + str(e))
        #     return "error:"+str(e)


if __name__ == "__main__":
    serverAddr = (serverIp, serverPort)

    fc = fileClient(serverAddr)
    # fileclient.sendFile('fromClientPath/file', 'toServerPath/file')
    # fileclient.recvFile('toClientPath/file', 'fromServerPath/file')
    fc.requestAllFile()
