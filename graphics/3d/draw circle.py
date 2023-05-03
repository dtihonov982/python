import graphics

from tkinter import *

circle = graphics.generate_circle(1, 30)

W = 200
H = 200

root = Tk()
root.minsize(width=W, height=H)
c = Canvas(root, width=W, height=H, bg='white')
c.pack()

circle = graphics.scaleEdges(circle, 50)
circle = graphics.transferEdges(circle, dx=W/2, dy=H/2)
graphics.draw(c, circle)
 
root.mainloop() 
