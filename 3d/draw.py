from tkinter import *

def draw(c, edges):
    for e in edges:
        px1 = e[0][0]
        py1 = e[0][1]
        px2 = e[1][0]
        py2 = e[1][1]
        c.create_line(px1, py1, px2, py2)