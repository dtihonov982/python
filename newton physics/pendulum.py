#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import Tk, Canvas, Frame, BOTH
from math import sin, cos, pi

g = 9.8
H = 300
W = 300
xc = H/2
yc = W/2

fps = 60
dt_mls = int(1000.0/fps)
dt = dt_mls/1000.0

class Pendulum:
    def __init__(self, x=0, y=0, L=150, R=10, a=pi/4, w=0):
        self.x = x
        self.y = y
        self.L = L
        self.R = R
        self.a = a
        self.w = w
        self.set_angle(a)

    def set_angle(self, a):
        self.x1 = self.x + sin(a)*self.L
        self.y1 = self.y + cos(a)*self.L

    def draw(self, canvas):
        canvas.create_line(self.x, self.y, self.x1, self.y1)
        canvas.create_oval(self.x1-self.R,
                           self.y1-self.R,
                           self.x1+self.R,
                           self.y1+self.R,
                           fill='black')
    
    def move(self, dt):
        self.a = self.a - self.w*dt
        self.w = self.w + sin(self.a)*g*dt/self.R
        self.set_angle(self.a)
    
    
 
class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent     
        self.canvas = Canvas(self)   
        self.initUI()
        
    def initUI(self):
        self.parent.title("Lines")        
        self.pack(fill=BOTH, expand=1)
 
        self.p = Pendulum(xc, yc/3)
        self.p.draw(self.canvas)
        
        self.canvas.pack(fill=BOTH, expand=1)
        self.timer()
    
    def timer(self):
        self.p.move(dt)
        self.canvas.delete('all')
        self.p.draw(self.canvas)
        self.canvas.after(dt_mls, self.timer)
 
if __name__ == '__main__':
    root = Tk()
    ex = Example(root)
    root.geometry("{}x{}+300+300".format(W, H))
    root.mainloop()  
