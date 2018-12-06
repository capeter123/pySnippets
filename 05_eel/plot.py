import eel
import random
import math

eel.init('web')                     # Give folder containing web files

window_inited = False
x = 0

@eel.expose                         # Expose this function to Javascript
def window_inited_py():
    print("true")
    global window_inited
    window_inited = True

@eel.expose
def get_init_data():
    return ["line1", "line2", "line3", "line4"]

@eel.expose
def update_data():
    global x
    x += 1
    y1 = random.randint(10,20)
    y2 = random.random()*20 + 5
    y3 = random.randint(1,30)
    y4 = 10 * math.sin(0.02 * math.pi * x)
    return [y1, y2, y3, y4]

# eel.window_inited()   # Call a Javascript function

eel.start('plot.html', size=(1000, 580))    # Start

