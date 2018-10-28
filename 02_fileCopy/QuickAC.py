import os
import shutil
import re

os.chdir(os.path.abspath(os.path.dirname(__file__)))


class QuicKAC():
    def __init__(self):
        self.personalitiesStr = 'SubsPers=m3mc.p_s\nAnalPers=m3mc.p_a\nCompPers=m3mc.p_c\n'
        self.outputRootStr = 'output'
        self.commonBlock = 'StartProjectMarker\nFolderName={}\nSourcePath={}\nOutputPath={}\n' + self.personalitiesStr + 'EndContainedFilesMarker\n'
        self.includes = ''
        self.file_P_S = ''
        self.file_P_A = '{}'
        self.file_P_C = ''

    def genQacProject(self, prjName='QAC'):
        if os.path.exists('QAC'):
            shutil.rmtree('QAC')
        os.mkdir('QAC')
        os.mkdir(os.path.join('QAC', 'output'))
        self.genPrjFile(prjName)
        self.genCfgFile(prjName)

    def genPrjFile(self, prjName='QAC'):
        blocks = []
        subProStartStr = 'StartSubProjectMarker\n'
        subProEndStr = 'EndSubProjectMarker\n'
        # # projectName
        # header = ''
        header = 'VersionTag45\n'
        # header += self.commonBlock
        # header = header.format(prjName, os.getcwd(), self.outputRootStr)
        blocks.append(header)

        childPath = []  # 记录子目录
        dealedhPath = []  # 记录处理过的含有.h文件的路径
        lastPath = ''  # 上一次处理的路径
        subProjectMarkerNum = 1  # 文件夹层数
        self.includes = ''
        # subProDealed = False
        subProStr = ''
        for pathname, dirnames, filenames in os.walk(os.getcwd()):
            print(pathname)
            # subProStr = ''
            folderStr = ''
            pathExsit = False
            FolderName = pathname.split('\\')[-1]
            SourcePath = pathname.replace(os.getcwd(), '')[1:]
            if pathname.find(os.getcwd() + '\\QAC') > -1:
                continue

            if pathname == os.getcwd():
                folderStr += self.commonBlock.format(
                    prjName, os.getcwd(),
                    self.outputRootStr)
            else:
                folderStr += self.commonBlock.format(
                    FolderName, SourcePath,
                    self.outputRootStr + '\\' + SourcePath)

            if (subProStr.find('SourcePath={}\n'.format(SourcePath)) == -1):
                pass
            else:
                pathExsit = True

            if len(dirnames) > 0:
                folderStr += subProStartStr
            for dirname in dirnames:
                if (pathname + '\\' + dirname).find(os.getcwd() + '\\QAC') > -1:
                    continue
                if pathname == os.getcwd():
                    folderStr += self.commonBlock.format(
                        dirname, dirname,
                        self.outputRootStr + '\\' + dirname)
                else:
                    folderStr += self.commonBlock.format(
                        dirname, SourcePath + '\\' + dirname,
                        self.outputRootStr + '\\' + SourcePath + '\\' + dirname)
            if folderStr.find(subProStartStr) > -1:
                folderStr += subProEndStr

            if subProStr == '':
                subProStr = folderStr
            elif pathExsit is True:
                # print(subProStr.find(self.__getSourcePathBlock(subProStr, SourcePath)),'========')
                subProStr = subProStr.replace(self.__getSourcePathBlock(subProStr, SourcePath), folderStr)

            print(subProStr)

            # cPath = ''
            # for filename in filenames:
            #     if str.lower(filename).endswith('.c'):
            #         cPath += pathname.replace(os.getcwd(),
            #                                   '')[1:] + '\\' + filename
            #         cPath += '\n'
            #     elif str.lower(filename).endswith('.h'):
            #         if pathname not in dealedhPath:
            #             dealedhPath.append(pathname)
            # commonStr += self.commonBlock.format(
            #     FolderName, SourcePath, self.outputRootStr + '\\' + SourcePath,
            #     cPath)

            # if pathname in childPath:
            #     subProDealed = True
            #     childPath.remove(pathname)
            # elif subProDealed is True:
            #     subProDealed = False

            # for dirname in dirnames:
            #     childPath.append(pathname + '\\' + dirname)

            # print(pathname, childPath)

        blocks.append(subProStr)

        self.includes = '\n'.join(
            ['-i "{}"'.format(item) for item in dealedhPath])

        prjFile = open('QAC\\' + prjName + '.txt', 'w')
        prjFile.writelines(blocks)
        prjFile.close()

    def __getSourcePathBlock(self, sourceStr, sourcePath):
        startIndex = 0
        block = ''
        while startIndex < len(sourceStr):
            index1 = sourceStr.find('StartProjectMarker', startIndex)
            index2 = sourceStr.find('EndContainedFilesMarker', startIndex)
            if index1 == -1 or index2 == -1:
                startIndex = len(sourceStr)
                continue
            startIndex = index2 + 24
            tmp = sourceStr[index1:startIndex]
            if tmp.find('SourcePath={}\n'.format(sourcePath)) > -1:
                block = tmp
                startIndex = len(sourceStr)
        return block

    def __insertSubProStrBySourcePath(self, soucreStr, sourcePath, subProStr):
        if soucreStr.find('SourcePath={}\n'.format(sourcePath)) == -1:
            return soucreStr

    def __editFilesBySourcePath(self, soucreStr, sourcePath, fileStr):
        if soucreStr.find('SourcePath={}\n'.format(sourcePath)) == -1:
            return soucreStr

    def genCfgFile(self, prjName='QAC'):
        with open('QAC\\m3mc.p_s', 'w') as psfile:
            psfile.write(self.file_P_S)
        with open('QAC\\m3mc.p_a', 'w') as pafile:
            pafile.write(self.file_P_A.format(self.includes))
        with open('QAC\\m3mc.p_c', 'w') as pcfile:
            pcfile.write(self.file_P_C)


if __name__ == '__main__':
    qc = QuicKAC()
    qc.genQacProject()