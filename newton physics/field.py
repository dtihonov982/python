#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import *
from math import sin, cos, pi, sqrt, atan
import numpy as np
from numpy.linalg import norm
from itertools import combinations
import time
import math

g = 9.8
H = 500.0
W = 800.0
xc = W/2
yc = H/2

fps = 25
dt_mls = int(1000.0/fps)
dt = dt_mls/1000.0

up_dt = 250

cps = fps*10
#dt_calc = 1.0/cps
dt_calc = 1/60

G = 10**3

K = 10**3

multiplex = 1

slowdown = 0.0


def curr_time():
    return int(round(time.time() * 1000))

prev_moment = curr_time()

class Field:
    def __init__(self, F):
        self.F = F
    def eval(self, x, y):
        return self.F(x, y)
    
    def draw(self, canvas):
        n = 15
        m = 15
        dy = H/n
        dx = W/n
        
        X = dx
        Y = dy
        for i in range(0, n-1):
            for j in range(0, m-1):
                ux, uy = self.F(X, Y)
                
                Ax = X
                Ay = Y
                Bx = ux+X
                By = uy+Y
                canvas.create_line(Ax, Ay, Bx, By, fill='blue', arrow=LAST)
                X += dx
            X = dx
            Y += dy
                
                
                

class Path:
    def __init__(self):
        self.max = 100
        self.list = []
    def add(self, x, y):
        self.list.append((x, y))
        if len(self.list) > self.max:
            del self.list[0]
    def draw(self, canvas, colour='red'):
        for i in range(0, len(self.list)-1):
            p1 = self.list[i]
            p2 = self.list[i+1]
            canvas.create_line(*p1, *p2, fill=colour)

class Path2:
    def __init__(self):
        self.max = 200
        self.list = []
        self.buffer = []
        self.color = 'red'
    def len(self):
        return len(self.list)
    def step_on(self, x, y, canvas):
        if self.len() == 0:
            self.buffer.append([x, y])
        if self.len() == 0 and len(self.buffer) == 1:
            x0 = self.buffer[0][0]
            y0 = self.buffer[0][1]
            tk_id = canvas.create_line(x0,
                                       y0,
                                       x,
                                       y,
                                       fill=self.color)
            self.list.append((x0, y0, x, y, tk_id))
            return
        if self.len() >= 1:
            #Last point
            p1 = self.list[self.len()-1]
            tk_id = canvas.create_line(p1[2],
                                       p1[3],
                                       x,
                                       y,
                                       fill=self.color)           
            self.list.append((p1[2], p1[3], x, y, tk_id))
            #Delete first line by id
            if self.len() > self.max:
                canvas.delete(self.list[0][4])
                del self.list[0]
class Path3:
    def __init__(self, color='blue'):
        self.last = []
        self.color = color
    def step_on(self, x, y, canvas):
        if len(self.last) == 0:
            self.last = [x, y]
            return
        if len(self.last) > 0:
            p = self.last
            canvas.create_line(p[0],
                               p[1],
                               x,
                               y,
                               fill=self.color)    
            self.last = [x, y]
            
class Body:
    def __init__(self, x=0, y=0, vx=0, vy=0, m=1, r=10, color='green'):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.m = m
        self.r = r
        self.id = None
        self.ax = 0
        self.ay = 0
        self.color = color
        self.path = Path2()
    def draw(self, canvas):
        self.id = canvas.create_oval(
            self.x-self.r,
            self.y-self.r,
            self.x+self.r,
            self.y+self.r,
            fill=self.color,
            outline='')
    def move(self, dt):
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt
        self.vx = self.vx + self.ax*dt
        self.vy = self.vy + self.ay*dt
    def move_pic(self, canvas):
        canvas.coords(self.id,
                      self.x-self.r,
                      self.y-self.r,
                      self.x+self.r,
                      self.y+self.r)
    def do_path(self, canvas):
        self.path.step_on(self.x, self.y, canvas)
    def get_point(self):
        return np.array([self.x, self.y], dtype=np.float32)
    def set_a(self, av):
        self.ax = av[0]
        self.ay = av[1]
    def get_v(self):
        return sqrt(self.vx**2+self.vy**2)
    #Расстояние до другого шара    
    def len(self, body):
        return sqrt((self.x-body.x)**2+(self.y-body.y)**2)
    #Проверяет, столкнулся ли шар с другим
    def hits(self, body):
        if self.len(body) > self.r+body.r:
            return False
        else:
            return True
    #Угол между прямой, соединяющей два шара, и осью Ох.
    def angle(self, body):
        if self.x != body.x:
            return atan((body.y-self.y)/(body.x-self.x))
        else:
            return 0
                
def transform(x, y, a):
    new_x = x*cos(a)-y*sin(a)
    new_y = x*sin(a)+y*cos(a)
    return (new_x, new_y)        

class Example(Frame):
  
    def __init__(self, parent, bodies=[], fields=[]):
        Frame.__init__(self, parent)   
        self.parent = parent     
        self.canvas = Canvas(self, background='white')   
        self.bodies = bodies
        self.monitor_str = StringVar()
        self.monitor = Label(parent, textvariable=self.monitor_str, justify=LEFT)
        
        self.fields = fields
        self.initUI()
        
    def initUI(self):
        self.parent.title("Lines")        
        self.pack(fill=BOTH, expand=1)
        
        self.monitor.place(x=W-100, y = 0)
        #self.monitor.pack()
        
        for b in self.bodies:
            b.draw(self.canvas)
        
        self.combs = list(combinations(self.bodies, 2))
        
        
        self.canvas.pack(fill=BOTH, expand=1)
        
    def start(self):
        for f in self.fields:
            f.draw(self.canvas)
            
        self.calc()
        self.draw()
        self.update_monitor()
    
    def calc(self):
        global prev_moment
        global slowdown
        slowdown = ((curr_time()-prev_moment)/(dt_calc*1000)-1)*100
        prev_moment = curr_time()
        
        dt_new = dt_calc/multiplex
        for i in range(0, multiplex):
            for b in self.bodies:
                b.move(dt_new)
                self.calculate()
                self.check()
                self.eval_fields()
        self.canvas.after(int(dt_calc*1000), self.calc)
    
    def draw(self):
        for b in self.bodies:
            b.move_pic(self.canvas)
            b.do_path(self.canvas)         
        #for f in self.fields:
            #f.draw(self.canvas)
        self.canvas.after(dt_mls, self.draw)
        
    def eval_fields(self):
        for b in self.bodies:
            for f in self.fields:
                ax, ay = f.eval(b.x, b.y)
                b.ax += ax
                b.ay += ay
                
    def update_monitor(self):
        #global prev_moment
        #slowdown = ((curr_time()-prev_moment)/up_dt-1)*100
        #prev_moment = curr_time()

        pool = []
        k = 1
        
        for b in self.bodies:
            curr = 'v{}: {:.1f}'.format(k, b.get_v())
            pool.append(curr)
            k += 1
        
        pool.append('slowdown: {:.1f}'.format(slowdown))
            
        self.monitor_str.set('\n'.join(pool))
        self.canvas.after(up_dt, self.update_monitor)
            
        
    def calculate(self):       
        N = len(self.bodies)    
        #Индекса списка
        for i in range(0, N):
            #Получить тело по индексу
            p = self.bodies[i]
            #Результирующее ускорение
            total_a = np.array([0, 0], dtype=np.float32)
            #Координаты текущего тела
            p_coords = p.get_point()
            #Для всех остальных индексов, не равных текущему
            for j in range(0, N):
                if j != i:
                    #Получить второе тело
                    q = self.bodies[j]
                    #Получить радиус-вектор соединяющий два тела,
                    #начало которого в центре первого тела.
                    r = q.get_point()-p_coords
                    #Получение компоненты ускорения
                    a = (G*q.m/((norm(r))**3))*r
                    total_a += a
                else:
                    pass
            p.set_a(total_a)
        
    def check(self):
        for pair in self.combs:
            a = pair[0]
            b = pair[1]
            
            #Расстояние между парой
            r = a.len(b)    
            #Тела коснулись или перекрыли друг друга
            dh = a.r + b.r - r
            if dh > 0:
                #Угол между телами
                angle = a.angle(b)
                #Сила реакции пропорциональна сближению
                #N = (a.r + b.r - r)*K
                #Воторой закон Ньютона. И третий.
                ax1 = -(K*dh/a.r)/a.m
                ax2 = (K*dh/b.r)/b.m
                #Получение проекций ускорений и прибавление их к существующему ускорению
                a.ax += ax1*cos(angle)
                a.ay += ax1*sin(angle)
                b.ax += ax2*cos(angle)
                b.ay += ax2*sin(angle)

def length(x, y):
    return sqrt(x**2+y**2)
                         
def rot_field(x, y):
    x1 = x-xc
    y1 = y-yc
    l = length(x1, y1)
    if l < 10:
        return (0, 0)
    else:
        H = 2
        hx = -H*y1/l
        hy = H*x1/l
        return (hx, hy)
    
def walls(x, y):
    H = 30
    d = 50
    if x < xc - d:
        return (H, 0)
    if x > xc + d:
        return (-H, 0)
    return (0, 0)
 
if __name__ == '__main__':
    root = Tk()
    
    f1 = lambda x, y: (0, -5)
    f = lambda x, y: (10, 10)
    b = [Body(W/3, yc, 0, 0, 1, 5, color='green')]
    
    ex = Example(root, b, fields=[Field(walls)])
    ex.start()
    root.geometry("{}x{}+100+100".format(int(W), int(H)))
    root.mainloop()  
