#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import Tk

from path import *
from body import *
from application import *
    
 
if __name__ == '__main__':
    root = Tk()
    
    #b0 = [
    #    Body(xc/2, yc, 0, -20), 
    #    Body(3*xc/2, yc, 0, 20)
    #    ]

    #Орбита эллиптическая
    b1 = [
        Body(xc, yc, 0, 0, 250000, 20),
        Body(xc-100, yc, 0, -60, 1, 5)
        ]
    
    #Орбита круглая
    V = 100
    R = 50
    b2 = [
        Body(xc, yc, 0, 0, V**2*R/G, 20, color='red'),
        Body(xc-R, yc, 0, -V, 1, 5)
        ]

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
    
    #3 тела
    
    trio = [
        Body(xc, yc, 0.0, u, M, 20.0),
        Body(xc-R-r, yc, 0.0, -V, m, 5.0),
        Body(xc+R, yc, 0.0, V/3, m, 5.0),
        ]   
    
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
    
    #Гравитационный трамплин
    V = 100
    d = 10
    R = 50
    M = 10**6
    
    trump = [
        Body(0, yc, V, 0, 1, 2),
        Body(xc, yc+d+R, 0, 0, M, R)
        ]        
    
    #Скопление
    m = 300
    r = 5
    vx = 25
    vy = 0
    b5 = []
    n = 5
    x = W/2
    y = H/6
    angle = 2*pi/n
    
    for i in range(0, n):
        b5.append(Body(x, y, vx, vy, m, r))
        x, y = transform(x-xc, y-yc, angle)
        vx, vy = transform(vx, vy, angle)
        x += xc
        y += yc
    
        


    
    ex = App(root, b5)
    ex.start()
    root.geometry("{}x{}+100+100".format(int(W), int(H)))
    root.mainloop()  
