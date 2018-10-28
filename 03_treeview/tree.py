import tkinter as tk
from tkinter import ttk, messagebox


def treeview_sort_column(tv, col, reverse):#Treeview、列名、排列方式
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)#排序方式
    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):#根据排序后索引移动
        tv.move(k, '', index)
        print(k)
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))#重写标题，使之成为再点倒序的标题

def brush_treeview(tv):
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
    for i in range(len(items)):
        if i % 2 == 1:
            tv.item(items[i], tags=('oddrow'))
    tv.tag_configure('oddrow', background='#eeeeff')

root = tk.Tk()
table = ttk.Treeview(
            root,
            show="headings",
            height=23,
            columns=['col-1', 'col-2', 'col-3', 'col-4'])
table.column(
                'col-1', width=50,
                anchor='w')  #表示列,不显示
table.heading('col-1', text='col-1', command=lambda: treeview_sort_column(table, 'col-1', False))  # set header text
table.heading('col-2', text='col-2')  # set header text
table.heading('col-3', text='col-3')  # set header text
table.heading('col-4', text='col-4')  # set header text
# self.table.bind("<<TreeviewSelect>>", self.on_tree_select)
# table.bind("<Button-1>", self.get_row_value)
table.pack(fill=tk.BOTH, expand=True)

items = table.get_children()
[table.delete(item) for item in items]

for i in range(20):
    table.insert('', 'end', val=(i, i**2, i**3, i**4))

brush_treeview(table)

root.mainloop()

