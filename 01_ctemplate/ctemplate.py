# ctemplate.py

import sys
import datetime


class ctemplate:

    __fileName = ' '
    __sourceName = ' '
    __headerName = ' '
    __time = datetime.datetime.now().strftime('%Y-%m-%d')
    __fileComments = {'@attention':' ',
                      '@date':__time,
                      '@version':'V01',
                      '@author':'Guangwei Huang',
                      '@file':" ",
    }

    __CommentsOrder = ('@file','@author','@date','@attention')

    def __init__(self,s):
        self.__fileName = s
        self.__sourceName = s + ".c"
        self.__headerName = s + '.h'
        self.__starter = '/*************************************************************************************\n'
        self.__end = '*************************************************************************************/\n\n'

    def generateCommentsAtTop(self,name):
        self.__fileComments['@file'] = name

        comments = self.__starter

        #find max length of string
        maxLen = 0
        for s in self.__CommentsOrder:
            if(len(s) > maxLen):
                maxLen = len(s)

        for k in self.__CommentsOrder:
            alignSpaceAmount = maxLen - len(k) + 4
            alignSpace = alignSpaceAmount * ' '
            comments += ('* '+ k + alignSpace + self.__fileComments[k] + '\n')
        comments += '* @Revision History\n' 
        comments += '------------------------------------------------------------------------------------\n' 
        comments += '* Version        Date         Author               Description\n'
        comments += '*-----------------------------------------------------------------------------------\n' 
        comments += '* 00.01.00       {0:<13}{1:<21}Initial Version\n\n'.format(self.__time, self.__fileComments['@author'])
        comments += self.__end + '\n'
        return comments

    def generateCommentsInTheEnd(self):
        return ("/*********************************** END OF FILE ************************************/\n")

    def createSource(self):
        fh = open(self.__sourceName, mode = 'w', encoding='utf-8')
        cm = self.generateCommentsAtTop(self.__sourceName)
        cm += self.__starter
        cm += '* INCLUDES\n'
        cm += self.__end
        cm += ("#include \"%s\"\n" %self.__headerName) 
        cm += self.__starter
        cm += '* VARIABLE DEFINITION AND DECLARATION\n'
        cm += self.__end
        cm += self.__starter
        cm += '* FUNCTION PROTOTYPES\n'
        cm += self.__end
        cm += '/* ============================================================================= *\n'
        cm += '* FUNCTION: void TEST(void)\n'
        cm += '* PURPOSE : \n'
        cm += '* INPUT:    NONE\n'
        cm += '* RETURN:   NONE\n'
        cm += '* Author:   {0}\n'.format(self.__fileComments['@author'])
        cm += '* Date:     {0}\n'.format(self.__fileComments['@date'])
        cm += '* ============================================================================== */\n'
        cm += ("\n"*5)
        cm += self.generateCommentsInTheEnd()
        fh.write(cm)
        fh.close()

    def createHeader(self):
        fh = open(self.__headerName,mode = 'w',encoding='utf-8')
        cm = self.generateCommentsAtTop(self.__headerName)
        cm += "#ifndef __%s_H\n" %self.__fileName.upper()
        cm += "#define __%s_H\n" %self.__fileName.upper()
        cm += self.__starter
        cm += '* INCLUDES\n'
        cm += self.__end
        cm += self.__starter
        cm += '* FUNCTION PROTOTYPES\n'
        cm += self.__end
        cm += self.__starter
        cm += '* GLOBAL CONSTANT MACROS\n'
        cm += self.__end
        cm += ("\n"*5)
        cm += "#endif\n"
        cm += self.generateCommentsInTheEnd()
        fh.write(cm)
        fh.close()

    def createTemplatePairs(self):
        self.createSource()
        self.createHeader()


if __name__ == '__main__':
        if len(sys.argv) != 2:
            sys.stderr.write("please input corret parameter")
        else:
            s = sys.argv[1]
            ct = ctemplate(s)
            ct.createTemplatePairs()