#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import Tk

from physics.body import *
from physics.application import *


if __name__ == '__main__':
    root = Tk()
    
    H = 500.0
    W = 500.0
    xc = H/2
    yc = W/2

    #Система из 2 тел
    R = 2*W/8
    r = R/10
    V = 100.0
    
    k = r/R
    u = k*V
    m = V**2*r*(1+k)**2/G
    M = V**2*R*(1+k)**2/G
    
    b3 = [
        Body(xc, yc, 0.0, u, M, 20.0),
        Body(xc-R-r, yc, 0.0, -V, m, 5.0)
        ]     
    
    ex = App(root, b3, W, H, fps=25)
    ex.start()
    root.geometry("{}x{}+100+100".format(int(W), int(H)))
    root.mainloop()  
