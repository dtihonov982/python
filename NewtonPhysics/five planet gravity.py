#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import Tk

from physics.body import *
from physics.application import *
    
 
if __name__ == '__main__':
    root = Tk()
    
    H = 500.0
    W = 800.0
    xc = W/2
    yc = H/2
    
    #Параметры тел
    m = 300
    r = 5
    vx = 25
    vy = 0
    b5 = []
    n = 5
    x = W/2
    y = H/6
    angle = 2*pi/n

    #Размещение тел на плоскости
    for i in range(0, n):
        b5.append(Body(x, y, vx, vy, m, r))
        x, y = rotate(x-xc, y-yc, angle)
        vx, vy = rotate(vx, vy, angle)
        x += xc
        y += yc

    
    ex = App(root, b5, W, H)
    ex.start()
    root.geometry("{}x{}+100+100".format(int(W), int(H)))
    root.mainloop()  
