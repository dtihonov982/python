from tkinter import *
from itertools import combinations
import time
import numpy as np
from math import sin, cos, pi, sqrt, atan
from numpy.linalg import norm

g = 9.80665
G = 10**3
K = 10**3

def curr_time():
    return int(round(time.time() * 1000))

class App(Frame):
  
    def __init__(self, parent, bodies=[], width = 800.0, height = 500.0, dt_calc = 1/60):
        Frame.__init__(self, parent)   
        self.parent = parent     
        self.canvas = Canvas(self)

        self.height = 500.0
        self.width = 800.0

        
        self.bodies = bodies
        self.combs = list(combinations(self.bodies, 2))

        self.dt_calc = dt_calc #частота пересчёта физики в секундах
        self.multiplex = 1 #частота обновления положения тел относительно пересчёта физики
        
        self.monitor_str = StringVar()
        self.monitor = Label(parent, textvariable=self.monitor_str, justify=LEFT)
        self.monitor_dt = 250 #частота пересчёта монитора в миллисекундах
        
        
        self.initUI()
        
    def initUI(self):
        self.parent.title("Lines")        
        self.pack(fill=BOTH, expand=1)
        #частота обновления экрана
        self.dt_mls = int(1000.0/25) 
        
        self.monitor.place(x=self.width-100, y = 0)
        
        for b in self.bodies:
            b.draw(self.canvas)

        self.canvas.pack(fill=BOTH, expand=1)
        
    def start(self):
        #Для расчёта slowdown 
        self.prev_moment = curr_time()
        self.slowdown = 0.0
        
        self.update()
        self.draw()
        self.update_monitor()
    
    def update(self):
        
        #Расчёт slowdown для монитора
        #slowdown отображает на сколько процентов реальный пересчет дольше dt_calc
        self.slowdown = ((curr_time()-self.prev_moment)/(self.dt_calc*1000)-1)*100
        self.prev_moment = curr_time()

        #dt_new - квант времени в секундах, передаваемый телу для обновления своих координат в соответствии с ускорением
        dt_new = self.dt_calc/self.multiplex
        #каждые dt_calc секунд физика пересчитывается multiplex раз
        for i in range(0, self.multiplex):
            for b in self.bodies:
                b.move(dt_new)
                self.update_acceleration()
                self.check_collision()
                
        self.canvas.after(int(self.dt_calc*1000), self.update)
    
    def draw(self):
        for body in self.bodies:
            body.move_pic(self.canvas)
            body.do_path(self.canvas)
            
        self.canvas.after(self.dt_mls, self.draw)
        
    
    def update_monitor(self):
        lines = []
        body_number = 1
        
        for b in self.bodies:
            curr_line = 'v{}: {:.1f}'.format(body_number, b.get_v())
            lines.append(curr_line)
            body_number += 1
        
        lines.append('slowdown: {:.1f}'.format(self.slowdown))
            
        self.monitor_str.set('\n'.join(lines))
        self.canvas.after(self.monitor_dt, self.update_monitor)
            
        
    def update_acceleration(self):       
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
        
    def check_collision(self):
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
