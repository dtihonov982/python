import reading
import geometry
import draw
from tkinter import *
from math import radians
from geometry import *

cube = reading.load_edges('Oxy.csv')

W = 500
H = 500
s = 100
timeout = int(1000/25)

root = Tk()
root.minsize(width=W, height=H)
c = Canvas(root, width=W, height=H, bg='white')
c.pack()

camera = Camera(z=-2, k=15, scale=100, width=W, height=H)

history = []

def keyup(e):
    global history
    if e.keycode in history:
        history.pop(history.index(e.keycode))

def keydown(e):
    global history
    if not e.keycode in history:
        history.append(e.keycode)
        
root.bind('<KeyPress>', keydown)
root.bind('<KeyRelease>', keyup)

move_sensitivity = 0.5
rotation_sensitivity = 0.1

keyForward = 87
keyLeft = 65
keyBack = 83
keyRight = 68
keyRightRot = 39
keyLeftRot = 37
keyUp = 38
keyDown = 40

def main_cycle():
    
    if keyForward in history:
        camera.z += move_sensitivity
        
    if keyBack in history:
        camera.z -= move_sensitivity
        
    if keyLeft in history:
        camera.x -= move_sensitivity
    
    if keyRight in history:
        camera.x += move_sensitivity
       
    if keyRightRot in history:
        camera.Ry += rotation_sensitivity
    
    if keyUp in history:
        camera.Rx += rotation_sensitivity
        
    if keyLeftRot in history:
        camera.Ry -= rotation_sensitivity
    
    if keyDown in history:
        camera.Rx -= rotation_sensitivity  
        
    c.delete('all')
    view = camera.getView(cube)
    draw.draw(c, view)    
    root.after(timeout, main_cycle)
    
root.after(0, main_cycle)
root.mainloop() 