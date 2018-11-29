# Tkinter Canvas Plotter
a plotter application using python tkinter canvas.   

![pic1](screenshots/animation2.gif)

you can simply initialize the plotter by following code.
```python
root = tk.Tk()
root.geometry('900x400')
frame = tk.Frame(root, width=900, height=300)
frame.pack(fill=tk.BOTH, expand=True)
plot = Plotter(frame)
```
- Dynamically resize to window size
- Save/load data files
- Draggable/Scalable signal
- Value tip for each signal
- Sort singal by the initialization order

These features may be helpful for signal plot. View source file for details.
