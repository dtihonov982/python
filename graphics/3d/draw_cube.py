import reading
import geometry
import draw
from tkinter import *
from math import radians
from geometry import *

cube = reading.load_edges('cube.csv')

W = 200
H = 200
s = 100

root = Tk()
root.minsize(width=W, height=H)
c = Canvas(root, width=W, height=H, bg='white')
c.pack()


dz = -2
dy = -H/2
dx = -W/2
k=2

print("begin")
printNodes(cube)

cube = transferEdges(cube, dz=-dz)
printNodes(cube)

cube = projectEdges(cube, k)

print("scale")
cube = scaleEdges(cube, s)
printNodes(cube)

cube = transferEdges(cube, dx=-dx, dy=-dy)



draw.draw(c, cube)
 
root.mainloop() 