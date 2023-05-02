import reading
import geometry
import draw
from tkinter import *

circle = reading.generate_circle(1, 30)

W = 200
H = 200

root = Tk()
root.minsize(width=W, height=H)
c = Canvas(root, width=W, height=H, bg='white')
c.pack()

circle = geometry.scaleEdges(circle, 50)
circle = geometry.transferEdges(circle, dx=W/2, dy=H/2)
draw.draw(c, circle)
 
root.mainloop() 