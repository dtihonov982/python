# -*- coding: utf-8 -*-
#Визуализация движения объектов под действием сил гравитации.

from tkinter import *
from math import sin, cos, pi, sqrt, atan
import numpy as np
from itertools import combinations
import time

#Параметры окна
H = 500
W = 800

#Координаты центра полотна
xc = W/2
yc = H/2

#Частота отрисовки
fps = 25
#Периодичность отрисовки в миллисекундах
dt_mls = int(1000.0/fps)
#Периодичность отрисовки в секундах
dt = dt_mls/1000.0

#Периодичность обновления табло в мсек
up_dt = 250

#Частота вычислений
cps = fps*10
#Период вычислений
dt_calc = 1/60

#Коэффициент гравитационного взаимодействия
G = 10**3
#Коэффициент упругого взаимодействия
K = 10**3

#Таймер имеет ограничение 1 мсек. Введя множитель и повторяя цикл за один такт таймера
#искусственно увеличивается частота пересчёта.
multiplex = 1

#Отображает в процентах замедление программы.
slowdown = 0.0

#Текущее время в миллисекундах
def curr_time():
    return int(round(time.time() * 1000))

#Для расчёта реального времени прошедшего с последнего такта.
prev_moment = curr_time()


#Исчезающий хвост
class Tail:
    def __init__(self, length=200, color='grey'):
        #Максимальное количество линий в хвосте
        self.length = length
        self.color = color
        self.last = None
        #Идентификаторы линий на холсте, составляющих хвост.
        self.lines = []

    def get_last(self):
        return self.last
        
    def len(self):
        return len(self.lines)
    
    def add(self, x, y, canvas):
        if self.last == None:
            self.last = (x, y)
            return

        new_id = canvas.create_line(self.last[0],
                                   self.last[1],
                                   x,
                                   y,
                                   fill=self.color)
        self.last = (x, y)
        self.lines.append(new_id)
            
        if self.len() > self.length:
            canvas.delete(self.lines[0])
            del self.lines[0]    

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
        self.tail = Tail()
        
    #Рисует круг на холсте в соответствии с его координатами
    def draw(self, canvas):
        if self.id == None:
            self.id = canvas.create_oval(
                self.x-self.r,
                self.y-self.r,
                self.x+self.r,
                self.y+self.r,
                fill=self.color,
                outline='')
        else:
            canvas.coords(self.id,
                          self.x-self.r,
                          self.y-self.r,
                          self.x+self.r,
                          self.y+self.r)     
            
    #Пересчитывает положение и скорость шара.
    def move(self, dt):
        self.x = self.x + self.vx*dt
        self.y = self.y + self.vy*dt
        self.vx = self.vx + self.ax*dt
        self.vy = self.vy + self.ay*dt

    #Дорисовывает хвост после передвижения тела
    def draw_tail(self, canvas):
        self.tail.add(self.x, self.y, canvas)
    #Получение координат тела в виде массива numpy
    def get_point(self):
        return np.array([self.x, self.y], dtype=np.float32)
    #Задает ускорение тела принимая массив numpy
    def set_a(self, av):
        self.ax = av[0]
        self.ay = av[1]
    #Возвращает модуль вектора скорости
    def get_v(self):
        return sqrt(self.vx**2+self.vy**2)
    #Возвращает модуль вектора ускорения
    def get_a(self):
        return sqrt(self.ax**2+self.ay**2)
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
                
#Поворачивает вектор на угол a
def transform(x, y, a):
    new_x = x*cos(a)-y*sin(a)
    new_y = x*sin(a)+y*cos(a)
    return (new_x, new_y)      

#Отображение на экране информации о состоянии объектов
class Monitor:
    def __init__(self, canvas, values={}):
        self._string = StringVar()
        self.values = values
        self.canvas = canvas
        self.label = Label(self.canvas, textvariable=self._string, justify=LEFT)
        #Положение - верхний правый угол, ширина 100
        self.label.place(x=W-100, y=0)
    #name - имя параметра
    #provider - функция, расчитывающая данный параметр
    def set(self, name, provider):
        self.values[name] = provider
    #Вызов всех функций - провайдеров и отрисовка значений
    def update(self):
        #Сборка строки
        parts = []
        for n, p in self.values.items():
            string = '{} = {:.0f}'.format(n, p())
            parts.append(string)
        self._string.set('\n'.join(parts))
   
            
class App(Frame):
  
    def __init__(self, parent, bodies=[]):
        Frame.__init__(self, parent)   
        self.bodies = bodies
        self.parent = parent     
        self.canvas = Canvas(self)   
        self.initUI()
        
    def initUI(self):
                
        self.parent.title("Bodies")        
        self.pack(fill=BOTH, expand=1)
        
        self.monitor = Monitor(self.canvas)   
        i = 1
        for b in self.bodies:
            b.draw(self.canvas)
            self.monitor.set('v'+str(i), b.get_v)
            self.monitor.set('a'+str(i), b.get_a)
            i += 1

        self.combs = list(combinations(self.bodies, 2))

        self.monitor.set('pairs', lambda: len(self.combs))
        
        self.canvas.pack(fill=BOTH, expand=1)
        
    def start(self):
        self.calc()
        self.draw()
        self.update_monitor()
        
    def draw(self):
        for b in self.bodies:
            b.draw(self.canvas)
            b.draw_tail(self.canvas)         
        self.canvas.after(dt_mls, self.draw)
    
    def calc(self):
        global prev_moment
        global slowdown
        slowdown = ((curr_time()-prev_moment)/(dt_calc*1000)-1)*100
        prev_moment = curr_time()
        
        dt_new = dt_calc/multiplex
        for i in range(0, multiplex):
            for b in self.bodies:
                b.move(dt_new)
                self.calcGravForce()
                self.calcElactic()
                
        self.canvas.after(int(dt_calc*1000), self.calc)

    def update_monitor(self):
        self.monitor.update()
        self.canvas.after(up_dt, self.update_monitor)
          
    def calcGravForce(self):       
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
                    R = q.get_point()-p_coords
                    #Получение компоненты ускорения
                    a = (G*q.m/((np.linalg.norm(R))**3))*R
                    total_a += a
                else:
                    pass
            p.set_a(total_a)
        
    def calcElactic(self):
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
    
    #Многоугольник
    m = 300
    r = 5
    vx = 30
    vy = 0
    b5 = []
    n = 3
    x = W/2
    y = H/6
    angle = 2*pi/n
    
    for i in range(0, n):
        b5.append(Body(x, y, vx, vy, m, r))
        x, y   = transform(x-xc, y-yc, angle)
        vx, vy = transform(vx, vy, angle)
        x += xc
        y += yc
    
    app = App(root, b5)
    app.start()
    
    #Параметры окна
    root.geometry('{}x{}+100+100'.format(W, H))
    root.mainloop()  
