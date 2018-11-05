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
                 canvas:tk.Canvas=None,
                 id=None,
                 offsety=0,
                 color='white',
                 history=10000):
        self.id = id
        self.tags = (id, )
        self._offsety = offsety
        self._offsetx = 0
        self._scaley = 1.0
        self.selected = False
        self.color = color
        self._lastx = 0
        self._lasty = 0
        self._lastoffsety = 0
        self._lastscaley = 1.0
        self._canvas = canvas
        self._canvasy = canvas.winfo_height() / 2 + 1
        self._history = history if history < 20000 else 20000
        self._points = []
        self._starty = 65535

    def setSelected(self, selected=False):
        self._canvas.lift(self.id)
        self.selected = selected
        _tags = list(self.tags)
        if selected:
            # _tags.append('selected')
            # self.tags = tuple(set(_tags))
            self._canvas.itemconfig(self.id, width=3, fill='white')
        elif not selected:
            # if 'selected' in _tags:
            #     _tags.remove('selected')
            # self.tags = tuple(_tags)
            self._canvas.itemconfig(self.id, width=1, fill=self.color)
    
    def setStatus(self, status):
        self._status = status

    def getStatus(self):
        return self._status

    def hide(self):
        self._canvas.itemconfig(self.id, state=tk.HIDDEN)
    
    def show(self):
        self._canvas.itemconfig(self.id, state=tk.NORMAL)

    def addLine(self, x, y):
        if self._starty is None:
            self._starty = y

        if self._canvas != None:
            if self._history != 0:
                if len(self._points) >= self._history:
                    del self._points[0]
                self._points.append(y)

                _lines = self._canvas.find_withtag(self.id)
                _linecnt = _lines.__len__()
                if _linecnt > self._history:
                    self._canvas.delete(_lines[0])
                    self._offsetx += 1 
                    for _line in _lines:
                        self._canvas.move(_line, -1, 0)

            offset_canvasy = self._canvasy + self._offsety
            self._canvas.create_line(
                (self._lastx - self._offsetx, (-self._lasty + offset_canvasy), x - self._offsetx,
                    (-y + offset_canvasy)),
                fill='white' if self.selected else self.color,
                width=3 if self.selected else 1,
                tags=self.tags,)
                # activewidth=1,
                # activefill='cyan')
            self._canvas.scale(self._canvas.find_withtag(self.id)[-1], 0, -self._starty+offset_canvasy, 1.0, self._scaley)
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

    def moveY(self, y=0):
        self._lastoffsety = self._offsety
        self._offsety += y
        for _line in self._canvas.find_withtag(self.id):
            self._canvas.move(_line, 0, y)

    def scaleY(self, scaley=1.0):
        if self._starty == 65535:
            return
        self._lastscaley = self._scaley
        self._scaley = self._scaley * scaley
        offset_canvasy = self._canvasy + self._offsety
        for _line in self._canvas.find_withtag(self.id):
            self._canvas.scale(_line, 0, -self._starty+offset_canvasy, 1.0, scaley)

    def restore(self):
        for _line in self._canvas.find_withtag(self.id):
            self._canvas.move(_line, 0, -self._offsety)
        self._offsety = 0
        self._scaley = 1.0


class Signal(Line):
    def __init__(
            self,
            canvas=None,
            id=None, **kwarg):
        Line.__init__(self, canvas=canvas, id=id, **kwarg)
        self.tags = (id, 'signal', )


class Ploter(Canvas):
    def __init__(self, parent:tk.Frame=None, interval=20, linenum=10, save=True):
        Canvas.__init__(self, parent, bg='#345', closeenough=2)
        parent.update_idletasks()
        self.pack(fill=tk.BOTH, expand=True)
        self.update_idletasks()
        self.bind("<Button-1>", self.__mouseDown)
        self.bind("<MouseWheel>", self._mouseScale)
        self.bind("<B1-Motion>", self.__mouseDownMove)
        self.bind("<B1-ButtonRelease>", self.__mouseUp)
        self.bind("<Enter>", self.__mouseEnter)
        self.bind("<Leave>", self.__mouseLeave)
        self.bind("<Motion>", self.__mouseHoverMove)
        self.__dataList = []
        self.x = 0
        self.offsety = 0
        self._interval = interval  # main loop interval to handle input data
        self._rulerOn = False
        self._dragOn = False
        self._gridOn = True
        self._loopOn = False
        self._ruler = None
        self._save = save
        self._lineNum = linenum
        # this data is used to keep track of an item being dragged
        # in this app, only vertical position 
        self._drag_data = {"sx":0, "sy":0, "x": 0, "y": 0, "item": None}
        self.__initLineList(self._lineNum)
        self.after(200, self.__initCanvas)

    def __main(self):
        if self._drag_data['item'] is None:
            pass
        else:
            _item = self._drag_data['item']
            if _item._lastoffsety != _item._offsety:
                pass
        self.after(20, self.__main)

    def __loop(self):
        if self._loopOn:
            self.after(self._interval, self.__loop)
        else:
            pass

    def __initCanvas(self):
        self.update_idletasks()
        self._width = self.winfo_width()
        self._height = self.winfo_height()
        self.drawGridLines(50)
        self.bind("<Configure>", self.__resize)
        self.__loop()

    def setLoopStatus(self, on=False):
        '''set the mainloop status
        
        Keyword Arguments:
            on {bool} -- status (default: {False})
        '''

        self._loopOn = on

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

    def setSignalTip(self, on=True):
        if on:
            maxlen = max([len(line.id) for line in self._lines])
            gap = (maxlen-2)*7
            gap = max(gap, 50)
            print(gap)
            for i, line in enumerate(self._lines):
                _row = int(i/5)
                _column = i%5
                self.create_rectangle(
                    10+gap*_column, 10+20*_row, gap*_column+20, 20*_row+20, fill=line.color, tags=('tip', 'tip'+line.id,))
                self.create_text(25 + gap*_column, 15+20*_row, text=line.id,
                                 fill='white', font=('微软雅黑', 8), tags=('tip', 'tip'+line.id,), anchor='w')
        else:
            if self.find_withtag('tip'):
                self.delete('tip')

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
    
    def getSignalbyId(self, id):
        '''根据id获取signal
        
        Arguments:
            id {str} -- signal id
        
        Returns:
            signal -- signal
        '''

        for _line in self._lines:
            if _line.id == id:
                return _line
        return None

    def getSignalbyTags(self, tags):
        '''根据tags获取signal
        
        Arguments:
            tags {list} -- 选中某个signal的时刻，该signal所具有的tags集合
                因为有id存在，能保证唯一性
        
        Returns:
            [signal] -- 信号
        '''

        for _line in self._lines:
            if set(_line.tags) & set(tags) == set(tags):  # 求交集
                return _line
        return None

    def _selectOneSignal(self, id):
        for _line in self._lines:
            if _line.id == id:
                _line.setSelected(True)
            else:
                _line.setSelected(False)

    def __initLineList(self, lineNumber):
        '''init all lines by given number
        
        Arguments:
            number {int} -- number of lines
        '''

        # self._color = []  #
        self._lines = []  #
        self._currentId = None  # 当前选择曲线id
        _list = list(colorList)
        while len(self._lines) < lineNumber:
            _index = random.randint(0, len(_list) - 1)
            _random = _list[_index]
            _list.remove(_random)
            _line = Signal(id=str(len(self._lines)), canvas=self,
                           history=10000, color=_random)
            self._lines.append(_line)

    def __resize(self, event):
        # self.update_idletasks()
        _deltay = (self.winfo_height() - self._height) / 2
        self.drawGridLines(50)
        for _line in self._lines:
            _line.setSelected(False)
            _line.moveY(_deltay)
        self._height = self.winfo_height()

    def _mouseScale(self, event):
        if self._drag_data["item"] is None:
            return
        if (event.delta > 0):
            self._drag_data["item"].scaleY(1.2)
        else:
            self._drag_data["item"].scaleY(0.8)

    # def updateLines(self, lineList:list):
    def __mouseDown(self, event):
        for signal in self._lines:
            signal.setSelected(selected=False)
        self._drag_data['item'] = None
        # print('down', event.x, event.y)
        # _items = self.find_closest(event.x, event.y)
        # print('closest', self.gettags(_items[0]))
        _items1 = self.find_overlapping(event.x-3, event.y-3, event.x+3, event.y+3)
        _currentItem = None
        for _item in _items1:
            if 'signal' in self.gettags(_item):
                _currentItem = _item
                break
        if _currentItem != None:
            _tags = self.gettags(_currentItem)
            print(_tags)
            self._drag_data['item'] = self.getSignalbyTags(_tags)
            self._drag_data['sy'] = event.y
            self._drag_data['sx'] = event.x
            self._drag_data['y'] = event.y
            self._drag_data['x'] = 0
            
            self._selectOneSignal(self._drag_data['item'].id)

    def __mouseDownMove(self, event):
        '''Handle dragging of an object'''
        if self._drag_data["item"] is None or self._dragOn is not True:
            return
        # compute how much the mouse has moved
        # delta_x = 0 # event.x - self._drag_data["x"]
        delta_y = event.y - self._drag_data["y"]
        # offset_y = event.y - self._drag_data["sy"]
        self._drag_data["item"].moveY(delta_y)
        # record the new position
        self._drag_data["x"] = 0
        self._drag_data["y"] = event.y

    def __mouseHoverMove(self, event):
        if self._rulerOn:
            delta_x = event.x - self.__rulerX
            self.after(80, self.__delayMove, delta_x)
            self.__rulerX = event.x
            # print(self.gettags(self.find_withtag(tk.CURRENT)))

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

        if len(self._lines) == self._lineNum:
            self._lines = []
            self._lines.append(Signal(id='Y1eqeqeqeqeqefrrrrrrq', canvas=self, history=100, color='#ff4'))
            self._lines.append(Signal(id='Y2', canvas=self, history=10000, color='#f40'))
            self._lines.append(Signal(id='Y3', canvas=self, history=10000, color='#4af'))
            self._lines.append(Signal(id='Y4', canvas=self, history=10000, color='#080'))
            self.setSignalTip()

        self._lines[0].addLine(self.x, y1)
        self._lines[1].addLine(self.x, y2)
        self._lines[2].addLine(self.x, y3)
        self._lines[3].addLine(self.x, y4)

        self.x = self.x + 1
        self.after(10, self._autoTest)

    def _toggleRuler(self):
        self._rulerOn = True if self._rulerOn is False else False

    def _toggleDrag(self):
        self._dragOn = True if self._dragOn is False else False

    def _toggleGrid(self):
        self._gridOn = True if self._gridOn is False else False
        self.drawGridLines(50)

    def _selectTest(self):
        _line = self._lines[random.randint(0, 3)]
        if _line.selected == True:
            _line.setSelected(False)
        else:
            _line.setSelected(True)

    def _restoreTest(self):
        self._lines[0].restore()
        self._lines[1].restore()
        self._lines[2].restore()
        self._lines[3].restore()

    def _scaleTest(self):
        _scale = random.randint(1, 3)
        if self._drag_data['item'] is not None:
            self._drag_data['item'].scaleY(_scale)

    def _tipTest(self):
        self.setSignalTip(on=False)


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
    tk.Button(root, text='restore', command=plot._restoreTest).pack(side=tk.LEFT)
    tk.Button(root, text='scale current', command=plot._scaleTest).pack(side=tk.LEFT)
    tk.Button(root, text='tip', command=plot._tipTest).pack(side=tk.LEFT)

    root.mainloop()
