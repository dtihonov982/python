from tkinter import *
from math import radians
from graphics import *

cube = load_edges('cube.csv')

W = 400
H = 300
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
cube = rotateEdges(cube, Rx=0.2, Rz=0.2)



draw(c, cube)
 
root.mainloop() 
