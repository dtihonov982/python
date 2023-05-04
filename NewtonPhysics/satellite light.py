#!/usr/bin/python
# -*- coding: utf-8 -*-

from tkinter import Tk

from path import *
from body import *
from application import *


          
 
if __name__ == '__main__':
    root = Tk()
    
    H = 500.0
    W = 800.0
    xc = W/2
    yc = H/2

    V = 200
    R = 50
    b2 = [
        Body(xc, yc, 0, 0, V**2*R/G, 20, color='red'),
        Body(xc-R, yc, 0, -V, 1, 5)
        ]


    
    ex = App(root, b2, W, H, dt_calc=0.001)
    ex.start()
    root.geometry("{}x{}+100+100".format(int(W), int(H)))
    root.mainloop()  
