# -*- coding: utf_8 -*-
import sys
import tkinter as tk 

class App:
    def __init__(self):
        self.root = tk.Tk('test')
        self.root.geometry('600x400')
        pass
    def setupWidget(self, fileName):
        self.file = fileName
        self.content = tk.StringVar()
        self.label = tk.Label(self.root, text=self.file)
        self.label.pack()
        self.text = tk.Entry(self.root, textvariable=self.content)
        self.text.pack()
        with open(self.file, mode='r') as file:
            contentList = file.readlines()
            allContent = ''
            for line in contentList:
                allContent += line+'\n'
            self.content.set(allContent)
        self.root.mainloop()
    def warning(self):
        self.label = tk.Label(self.root, text='请输入合法参数')
        self.label.pack()
        self.root.mainloop()

if __name__ == '__main__':
    app = App()
    if len(sys.argv) == 2:
        app.setupWidget(sys.argv[1])
    else:
        app.warning()
