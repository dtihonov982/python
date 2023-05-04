#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import *
from physics.body import *
from physics.application import *


if __name__ == '__main__':
    root = Tk()
    G = 10**3
    H = 500.0
    W = 800.0
    xc = W/2
    yc = H/2
    
    #2 орбиты
    V = 100
    r = W/10
    R = 3*W/8
    m = 1
    
    u = V*sqrt(r/R)
    M = V**2*r/G
    
    orb = [
        Body(xc, yc, 0.0, 0.0, M, 10),
        Body(xc+r, yc, 0.0, V, m, 2),
        Body(xc+R, yc, 0.0, u, m, 2)
        ]        
    
    L0 = 500
    m = 0.01
    v = 100
    R = 10
    d = 0
    face_to_face = [
        Body(xc-L0/2, yc+d, v, 0, m, R),
        Body(xc+L0/2, yc-d, -v, 0, m, R)
        ]

    
    ex = App(root, face_to_face, fps=25, dt_calc=0.001)
    ex.start()
    root.geometry("{}x{}+100+100".format(int(W), int(H)))
    root.mainloop()  
