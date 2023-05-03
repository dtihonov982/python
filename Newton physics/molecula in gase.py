#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import Tk, Canvas, Frame, BOTH
from random import random, randint
import math
from itertools import combinations

#Радиус шара
color = 'blue'
#Модуль скорости шара
vabs = 5
#Количество шаров
N = 150

H = 330
W = 330
#Периодичность обновления экрана в мск
T = 25

class Ball:
    def __init__(self, x=W/2, y=H/2, vx=0, vy=0, tk_id=None, r = 2):
        self.r = r
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        #Идентификатор шара на холсте
        self.tk_id = tk_id

    #Расстояние до другого шара    
    def len(self, ball):
        return math.sqrt((self.x-ball.x)**2+(self.y-ball.y)**2)

    #Проверяет, столкнулся ли шар с другим
    def hits(self, ball):
        if self.len(ball) > self.r+ball.r:
            return False
        else:
            return True

    #Угол между прямой, соединяющей два шара, и осью Ох.
    def angle(self, ball):
        if self.x != ball.x:
            return math.atan((ball.y-self.y)/(ball.x-self.x))
        else:
            return 0 

class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent        
        self.initUI()

        self.balls = []

    def initUI(self):
        self.parent.title("Shapes")        
        self.pack(fill=BOTH, expand=1)
 
        self.canvas = Canvas(self)
        self.canvas.pack(fill=BOTH, expand=1)

    def generate(self):
        first = True
        for i in range(0, N):
            nb = Ball()
            
            #Случайное размещение шара
            nb.x = randint(0+nb.r, W-nb.r)
            nb.y = randint(0+nb.r, H-nb.r)           
            nb.tk_id = self.canvas.create_oval(
                nb.x-nb.r,
                nb.y-nb.r,
                nb.x+nb.r,
                nb.y+nb.r,
                outline='',
                fill=('red' if first else color), width=0)
            first = False

            #Назначение случайной скорости.
            #Скорости всех шаров равны по величине и отличаются по направлению.
            
            #Произвольный угол в диапазоне [0; 2pi]
            phi = random() * 2* math.pi
            
            nb.vx = math.cos(phi) * vabs
            nb.vy = math.sin(phi) * vabs          

            self.balls.append(nb)
            #Расчёт всех возможных пар шаров для последующей проверки столкновений
            self.combs = list(combinations(self.balls, 2))

    def set(self, data):
        for ball in data:
            nb = Ball()
            nb.x = ball[0]
            nb.y = ball[1]            
            nb.vx = ball[2]
            nb.vy = ball[3]
            nb.tk_id = self.canvas.create_oval(
                nb.x-nb.r,
                nb.y-nb.r,
                nb.x+nb.r,
                nb.y+nb.r,
                outline='',
                fill=color, width=0)
            self.balls.append(nb)

        self.combs = list(combinations(self.balls, 2))
        

        
    def start(self):
        #Движение шаров
        for i in range(0, len(self.balls)):
            b = self.balls[i]
            b.x += b.vx
            b.y += b.vy
            self.canvas.move(b.tk_id, b.vx, b.vy)

        self.check()
        self.check_wall()
        
        self.canvas.after(T, self.start)

    def check(self):
        for pair in self.combs:
            a = pair[0]
            b = pair[1]
                
            #print('Collision! ({}, {}), ({}, {}): {}-{}'.format(a.x, a.y, b.x, b.y, a.len(b), a.hits(b)))
            if a.hits(b):
                angle = a.angle(b)
                avx2, avy2 = transform(a.vx, a.vy, -angle)
                bvx2, bvy2 = transform(b.vx, b.vy, -angle)
                #Если шары движутся навстречу
                if avx2 - bvx2 > 0:
                
                    buff = 0
                    buff = bvx2
                    bvx2 = avx2
                    avx2 = buff

                    a.vx, a.vy = transform(avx2, avy2, angle)
                    b.vx, b.vy = transform(bvx2, bvy2, angle)

    def check_wall(self):
        for b in self.balls:
            if (b.x > W - b.r and b.vx > 0) or (b.x < b.r and b.vx < 0):
                b.vx = -b.vx
            if (b.y > H - b.r and b.vy > 0) or (b.y < b.r and b.vy < 0):
                b.vy = -b.vy             
       
    def test(self):
        pass
        
def transform(x, y, a):
    new_x = x*math.cos(a)-y*math.sin(a)
    new_y = x*math.sin(a)+y*math.cos(a)
    return (new_x, new_y)

if __name__ == '__main__':
    root = Tk()
    ex = Example(root)
    root.geometry("{}x{}+300+300".format(W, H))
    
    ex.generate()
    xc = W/2
    yx = H/2
    r = 10

    #ex.set([[r, H/2, 1, 1]])
    #Фронтальный удар
    #ex.set([[xc-35, yx, 1, 0], [xc+35, yx, -1, 0]])
    #Перекрытие
    #ex.set([[xc-5, yx, 1, 0], [xc+5, yx, -1, 0]])
    #Косой удар
    #ex.set([[xc-35, yx, 1, 0], [xc+35, yx+r, -1, 0]])
    #Двойной удар
    #ex.set([[xc-35, yx, 1, 0], [xc+35, yx+r, 0, 0], [xc+35, yx-r, 0, 0]])
    #Перекрытие со стеной
    #ex.set([[r/2, H/2, 1, 0]])
    
    ex.start()
    root.mainloop()
