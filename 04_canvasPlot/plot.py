import tkinter as tk
import time, random, math
import os
from tkinter import Canvas
from threading import Thread
import random

lasty1, lasty2, lasty3, lasty4, lastx = 0, 0, 0, 0, 0
testLines = []

colorList = ('#FFA54F', '#FF83FA', '#FF4500', '#FDF5E6', '#F08080', '#EEE9E9',
             '#EEDC82', '#EED2EE', '#D02090', '#D1EEEE', '#DDA0DD', '#CAFF70',
             '#CAE1FF', '#CD6600', '#C1FFC1', '#CCCCCC', '#BBFFFF', '#BF3EFF',
             '#A2CD5A', '#76EEC6', '#4876FF', '#00CD00', '#228B22', '#20B2AA',
             '#228B22', '#8B7B8B', '#CDC673')


class Line:
    def __init__(self,
                 canvas=None,
                 id=None,
                 offsetY=0,
                 color='white',
                 history=10000):
        self.id = id
        self.tags = (id, )
        self.offsetY = offsetY
        self.selected = False
        self.color = color
        self._lastx = 0
        self._lasty = 0
        self._canvas = canvas
        self._history = history
        self._points = []

    def setSelected(self, selected=False):
        self.selected = selected
        _tags = list(self.tags)
        print(_tags)
        if selected:
            _tags.append('selected')
            self.tags = tuple(set(_tags))
            self._canvas.itemconfig(self.id, width=3, fill='white')
        elif not selected:
            if 'selected' in _tags:
                _tags.remove('selected')
            self.tags = tuple(_tags)
            self._canvas.itemconfig(self.id, width=1, fill=self.color)

    def addLine(self, x, y):
        if self._canvas != None:
            if self._history != 0:
                if len(self._points) >= self._history:
                    del self._points[0]
                self._points.append((x, y))

            offset_canvasy = self._canvas.winfo_height(
            ) / 2 + 1 + self.offsetY
            self._canvas.create_line(
                (self._lastx, -self._lasty + offset_canvasy, x,
                    -y + offset_canvasy),
                fill='white' if self.selected else self.color,
                width=3 if self.selected else 1,
                tags=self.tags)
            self._lastx = x
            self._lasty = y

    def configTag(self, tag):
        '''config line tag name
        if exsited, remove it
        else add it to tags tuple
        
        Arguments:
            tag {str} -- tag name
        '''
        _tags = list(self.tags)
        if tag not in _tags:
            self.tags = tuple(_tags.append(tag))
        else:
            self.tags = tuple(_tags.remove(tag))

    def setOffsetY(self, offsety=0):
        self.offsetY = offsety


class Signal(Line):
    def __init__(
            self,
            canvas=None,
            id=None, **kwarg):
        Line.__init__(self, canvas=canvas, id=id, **kwarg)
        self.tags = (id, 'signal', )


class Ploter(Canvas):
    def __init__(self, parent: tk.Frame=None, interval=20):
        Canvas.__init__(self, parent, bg='#345')
        parent.update_idletasks()
        self.pack(fill=tk.BOTH, expand=True)
        self.bind("<Button-1>", self.__mouseDown)
        self.bind("<B1-Motion>", self.__mouseDownMove)
        self.bind("<B1-ButtonRelease>", self.__mouseUp)
        self.bind("<Enter>", self.__mouseEnter)
        self.bind("<Leave>", self.__mouseLeave)
        self.bind("<Motion>", self.__mouseHoverMove)
        self.__dataList = []
        self.x = 0
        self.offsetY = 0
        self._interval = interval
        self._rulerOn = False
        self._dragOn = False
        self._gridOn = True
        self._ruler = None
        self._maxLineNum = 10
        self.__initLineList(self._maxLineNum)
        self.after(100, self.drawGridLines)

    def __loop(self):
        pass

    def setLoopStatus(self, on=False):
        '''set the mainloop status
        
        Keyword Arguments:
            on {bool} -- status (default: {False})
        '''

        self._status = on

    def setDrag(self, on=False):
        '''enable or disable the mouse drag
        
        Keyword Arguments:
            on {bool} -- status (default: {False})
        '''

        self._dragOn = on

    def setRuler(self, on=False):
        '''show or hide coordinates when mouse move
        
        Keyword Arguments:
            on {bool} -- true for show ruler (default: {False})
        '''

        self._rulerOn = on

    def setInterval(self, interval=20):
        '''set mainloop interval
        
        Keyword Arguments:
            interval {int} -- interval (default: {20})
        '''

        self._interval = interval

    def setGrid(self, on=True):
        '''show or hide the grids
        
        Keyword Arguments:
            on {bool} -- true for show grid lines (default: {True})
        '''

        self._gridOn = on

    def clearstrip(self, p, color):  # Fill strip with background color
        self.bg = color  # save background color for scroll
        self.data = None  # clear previous data
        self.x = 0
        p.tk.call(p, 'put', color, '-to', 0, 0, p['width'], p['height'])

    def drawGridLines(self, width=50):
        offsety = math.floor(self.winfo_height() / 2) + 1
        offsetx = self.winfo_width()
        __grid = self.find_withtag('grid')
        if __grid:
            self.delete('grid')
        self.create_line(
            (0, offsety, offsetx, offsety),
            fill="#708090",
            dash=(2, 6),
            tags=('grid'))
        if self._gridOn is True:
            xnum = math.floor(self.winfo_width() / width)
            for i in range(xnum):
                self.create_line(
                    (i * 50 + 50, 0, i * 50 + 50, self.winfo_height()),
                    fill="#708090",
                    dash=(1, 6),
                    tags=('grid'))
            ynum = math.floor(self.winfo_height() / (2 * width))
            for j in range(ynum):
                self.create_line(
                    (0, j * 50 + 50 + offsety, self.winfo_width(),
                     j * 50 + 50 + offsety),
                    fill="#708090",
                    dash=(2, 6),
                    tags=('grid'))
                self.create_line(
                    (0, -j * 50 - 50 + offsety, self.winfo_width(),
                     -j * 50 - 50 + offsety),
                    fill="#708090",
                    dash=(2, 6),
                    tags=('grid'))

    def __initLineList(self, maxNumber):
        '''init all lines by given max number
        
        Arguments:
            number {int} -- number of lines
        '''

        self._color = []  #
        self._lineId = [None] * maxNumber  #
        self._currentId = None  # 当前选择曲线id
        _list = list(colorList)
        while len(self._color) < maxNumber:
            _index = random.randint(0, len(_list) - 1)
            print(_index, len(_list))
            _random = _list[_index]
            _list.remove(_random)
            self._color.append(_random)

    # def updateLines(self, lineList:list):
    def __mouseDown(self, event):
        print(event.x, event.y)
        # _items = self.find_closest(event.x, event.y)
        # print('closest', self.gettags(_items[0]))
        _items1 = self.find_overlapping(event.x-3, event.y-3, event.x+3, event.y+3)
        _currentItem = None
        for _item in _items1:
            if 'signal' in self.gettags(_item):
                _currentItem = _item
                break
        print(self.gettags(_currentItem))

    def __mouseDownMove(self, event):
        # print(event.x, event.y)
        pass

    def __mouseHoverMove(self, event):
        if self._rulerOn:
            delta_x = event.x - self.__rulerX
            self.after(80, self.__delayMove, delta_x)
            self.__rulerX = event.x

    def __delayMove(self, delta_x):
        self.move(self._ruler, delta_x, 0)

    def __mouseUp(self, event):
        print(event.x, event.y)

    def __mouseEnter(self, event):
        if self._rulerOn:
            self._ruler = self.create_line(
                (event.x, 0, event.x, self.winfo_height()), fill="#FFFAFA")
            self.__rulerX = event.x

    def __mouseLeave(self, event):
        if self._ruler is not None:
            self.delete(self._ruler)

    # below code just for test

    def _autoTest(self):
        y1 = 10 * math.sin(0.02 * math.pi * self.x)
        y2 = 9 + 5 * (random.random() - 0.5)
        y3 = 50
        y4 = -30 if (self.x % 20 == 0) else 20

        if len(testLines) == 0:
            testLines.append(Signal(id='Y1', canvas=self, history=10000, color='#ff4'))
            testLines.append(Signal(id='Y2', canvas=self, history=10000, color='#f40'))
            testLines.append(Signal(id='Y3', canvas=self, history=10000, color='#4af'))
            testLines.append(Signal(id='Y4', canvas=self, history=10000, color='#080'))

        testLines[0].addLine(self.x, y1)
        testLines[1].addLine(self.x, y2)
        testLines[2].addLine(self.x, y3)
        testLines[3].addLine(self.x, y4)

        self.x = self.x + 1
        self.after(self._interval, self._autoTest)

    def _toggleRuler(self):
        self._rulerOn = True if self._rulerOn is False else False

    def _toggleDrag(self):
        self._dragOn = True if self._dragOn is False else False

    def _toggleGrid(self):
        self._gridOn = True if self._gridOn is False else False
        self.drawGridLines(50)

    def _selectTest(self):
        # items = self.find_withtag('signal')
        # selected = items[random.randint(0, len(items) - 1)]
        # tagList = list(self.gettags(selected))
        # tagList.remove('signal')
        # print(tagList[0])
        # self.itemconfig(tagList[0], width=3, fill='white')
        global testLines
        _line = testLines[random.randint(0, 3)]
        if _line.selected == True:
            _line.setSelected(False)
        else:
            _line.setSelected(True)


if __name__ == '__main__':

    root = tk.Tk()
    root.geometry('900x400')
    frame = tk.Frame(root, width=900, height=300)
    frame.pack(fill=tk.BOTH, expand=True)

    plot = Ploter(frame)

    tk.Button(root, text='start', command=plot._autoTest).pack(side=tk.LEFT)
    tk.Button(root, text='ruler', command=plot._toggleRuler).pack(side=tk.LEFT)
    tk.Button(root, text='drag', command=plot._toggleDrag).pack(side=tk.LEFT)
    tk.Button(root, text='grid', command=plot._toggleGrid).pack(side=tk.LEFT)
    tk.Button(root, text='select', command=plot._selectTest).pack(side=tk.LEFT)

    root.mainloop()
