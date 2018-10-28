import os
import zipfile
import tkinter as tk
from tkinter import messagebox, ttk
import shutil

os.chdir(os.path.realpath(os.path.dirname(__file__)))

################## config start ########################
copyList = (
    '22222',
    '33333',
    '44444',
    '55555555555555555',
    '777777777',
    '8888888888',
    'xml.py',
    '999999',
    '666666666666'
)
################### config end #########################

class packFile:
    def __init__(self):
        self.__setupWidget()

    def __setupWidget(self):
        self.window = tk.Tk()
        self.window.title('ZipLib')
        w, h = 275, 180
        # 获取屏幕 宽、高
        ws = self.window.winfo_screenwidth()
        hs = self.window.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2) - 20
        self.window.geometry('{}x{}+{}+{}'.format(w, h, int(x), int(y)))
        self.window.resizable(0, 0)  # 防止窗口调整大小

        self.__targetFolder = tk.StringVar()
        tk.Label(self.window, text='文件夹', font=('微软雅黑', 10)).grid(row=0, column=0, padx=5, pady=10)
        tk.Entry(self.window, textvariable=self.__targetFolder, font=('微软雅黑', 10), width=20).grid(row=0, column=1)
        self.__targetFolder.set('ZipLib')

        tk.Button(self.window, text='确认', font=('微软雅黑', 10), width=4, command=self.__packFiles).grid(row=0, column=2, padx=5)

        self.table = ttk.Treeview(
            self.window,
            show="headings",
            height=5,
            columns=('File', 'Result'))
        self.table.column(
                'File', width=175,
                anchor='w')  #表示列,不显示
        self.table.heading('File', text='File')  #显示表头
        self.table.column(
                'Result', width=80,
                anchor='center')  #表示列,不显示
        self.table.heading('Result', text='Result')  #显示表头
        self.table.grid(row=1, column=0, columnspan=3, padx=5)

        self.window.mainloop()

    def brush_treeview(self, tv):
        """
        改变treeview样式
        :param tv:
        :return:
        """
        if not isinstance(tv, ttk.Treeview):
            raise Exception(
                "argument tv of method bursh_treeview must be instance of ttk.TreeView"
            )
        #=============设置样式=====
        items = tv.get_children()
        for item in items:
            item_text = self.table.item(item, "values")
            if item_text[1] == 'failed':
                tv.item(item, tags=('fail'))
            else:
                tv.item(item, tags=('success'))
        tv.tag_configure('fail', background='#EEB4B4')
        tv.tag_configure('success', background='#C1FFC1')

    def zip_ya(self):
        startdir = self.__targetFolder.get()  #要压缩的文件夹路径
        file_news = startdir +'.zip' # 压缩后文件夹的名字
        z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
        for dirpath, dirnames, filenames in os.walk(startdir):
            fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
            fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                z.write(os.path.join(dirpath, filename),fpath+filename)
        self.table.insert("", "end", values=[file_news, 'success'])
        self.brush_treeview(self.table)
        z.close()

    def __packFiles(self):
        items = self.table.get_children()
        [self.table.delete(item) for item in items]
        folder = self.__targetFolder.get()
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)
        for filename in copyList:
            vals = [filename.split('\\')[-1],'']
            if os.path.isfile(filename):
                shutil.copy(filename, folder)
                vals[1] = 'success'
            else:
                vals[1] = 'failed'
            self.table.insert("", "end", values=vals)
            self.brush_treeview(self.table)
        self.zip_ya()
        shutil.rmtree(folder)

if __name__ == '__main__':
    pf = packFile()