from path import Path2, Path3
from math import sin, cos, pi, sqrt, atan

import numpy as np



class Body:
    def __init__(self, x=0, y=0, vx=0, vy=0, m=1, r=10, color='green'):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        #mass
        self.m = m
        
        self.r = r
        self.id = None
        #acceleration
        self.ax = 0
        self.ay = 0
        
        self.color = color
        #trace
        self.path = Path2()

    #draws circle
    def draw(self, canvas):
        self.id = canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill = self.color,
            outline='')
        
    def move(self, dt):
        self.x = self.x + self.vx * dt
        self.y = self.y + self.vy * dt
        self.vx = self.vx + self.ax * dt
        self.vy = self.vy + self.ay * dt
        
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
                
def rotate(x, y, a):
    new_x = x*cos(a)-y*sin(a)
    new_y = x*sin(a)+y*cos(a)
    return (new_x, new_y)  
