#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import *
from math import sin, cos, pi, sqrt, atan
import numpy as np
from numpy.linalg import norm
from itertools import combinations
import time
from path import *

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
        self.color = 'blue'
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
  
    def __init__(self, parent, bodies=[]):
        Frame.__init__(self, parent)   
        self.parent = parent     
        self.canvas = Canvas(self)   
        self.bodies = bodies
        self.monitor_str = StringVar()
        self.monitor = Label(parent, textvariable=self.monitor_str, justify=LEFT)
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
        self.canvas.after(int(dt_calc*1000), self.calc)
    
    def draw(self):
        for b in self.bodies:
            b.move_pic(self.canvas)
            b.do_path(self.canvas)         
        self.canvas.after(dt_mls, self.draw)
        
    
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
    
        


    
    ex = Example(root, b5)
    ex.start()
    root.geometry("{}x{}+100+100".format(int(W), int(H)))
    root.mainloop()  
