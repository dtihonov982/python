import reading
import geometry
import draw
from tkinter import *
from math import radians
from geometry import *

cube = reading.load_edges('cube.csv')

W = 500
H = 500
s = 100
timeout = int(1000/25)

root = Tk()
root.minsize(width=W, height=H)
c = Canvas(root, width=W, height=H, bg='white')
c.pack()

camera = Camera(z=-2, k=2, scale=100, width=W, height=H)

view = camera.getView(cube)

draw.draw(c, view)


def main_cycle():
    
    root.after(timeout, main_cycle)
    

 
root.after(0, main_cycle)
root.mainloop() 