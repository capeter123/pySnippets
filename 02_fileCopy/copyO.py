import shutil
import os
import sys

os.chdir(os.path.abspath(os.path.dirname(__file__)))

def GenConfigFile():
    fileConfig = open('obj2copy.txt', mode='w')
    for parent,dirnames,fileNames in os.walk(os.getcwd()):
        for fileName in fileNames:
            if __file__.find(fileName) > -1:
                continue
            fileConfig.write(fileName + '\n')
    fileConfig.close()


def CopyObjFile(dst: str):
    with open('obj2copy.txt', mode='r') as file:
        fileList = file.readlines()
        for fileName in fileList:
            path = os.getcwd() + "\\" + fileName.strip()
            if os.path.exists(path):
                shutil.copy(path, dst)
        # path = os.listdir(os.getcwd())

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'EPS':
            shutil.rmtree('FuncObj_EPS', ignore_errors=True)
            os.mkdir('FuncObj_EPS')
            CopyObjFile(os.getcwd() + '\\FuncObj_EPS')
        elif sys.argv[1] == 'ACM':
            shutil.rmtree('FuncObj_ACM', ignore_errors=True)
            os.mkdir('FuncObj_ACM')
            CopyObjFile(os.getcwd() + '\\FuncObj_ACM')
    else:
        GenConfigFile()