from tkinter import *
from itertools import combinations
import time
import numpy as np
from numpy.linalg import norm

g = 9.8
H = 500.0
W = 800.0
xc = W/2
yc = H/2


dt_calc = 1/60
fps = 25
dt_mls = int(1000.0/fps)
dt = dt_mls/1000.0

up_dt = 250

cps = fps*10
#dt_calc = 1.0/cps

G = 10**3

K = 10**3

multiplex = 1

slowdown = 0.0

def curr_time():
    return int(round(time.time() * 1000))

prev_moment = curr_time()

class App(Frame):
  
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
