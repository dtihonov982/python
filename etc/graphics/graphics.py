# -*- coding: utf-8 -*-
import numpy as np
from math import sin, cos, radians

#Список ребер edges должен представлять собой list, содержащий
#list из двух элементов np.array, представляющий собой точки.
#Массив должен содержать 4-ый элемент, равный единице.

def transformEdges(edges, T):
    new_edges = []
    for e in edges:
        new_e = []
        for p in e:
            new_p = p.dot(T)
            new_e.append(new_p/new_p[3])
        new_edges.append(new_e)
    return new_edges
    

def getTransferMatrix(dx, dy, dz):
    return np.array([
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [dx, dy, dz, 1]
                        ])

def getTurnZMatrix(angle):
    return np.array([
                        [cos(angle), sin(angle), 0, 0],
                        [-sin(angle), cos(angle), 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]
                        ])

def getTurnXMatrix(angle):
    return np.array([
                        [1, 0, 0, 0],
                        [0, cos(angle), sin(angle), 0],
                        [0, -sin(angle), cos(angle), 0],
                        [0, 0, 0, 1]
                        ])

def getTurnYMatrix(angle):
    return np.array([
                        [cos(angle), 0, -sin(angle), 0],
                        [0, 1, 0, 0],
                        [sin(angle), 0, cos(angle), 0],
                        [0, 0, 0, 1]
                        ])

#Центром прекции является точка (0, 0, -k)
def getProjectionMatrix(k):
    return np.array([
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 0, 1/k],
                        [0, 0, 0, 1]
                        ])    

def getScaleMatrix(S):
    return np.array([
                        [S, 0, 0, 0],
                        [0, S, 0, 0],
                        [0, 0, S, 0],
                        [0, 0, 0, 1]
                        ])   

def transferEdges(edges, dx=0., dy=0., dz=0.):
    T = getTransferMatrix(dx, dy, dz)
    return transformEdges(edges, T)

def rotateEdges(edges, Rx=0., Ry=0., Rz=0.):
    Rx = getTurnXMatrix(Rx)
    Ry = getTurnYMatrix(Ry)
    Rz = getTurnZMatrix(Rz)
    R = Rx.dot(Ry.dot(Rz))
    return transformEdges(edges, R)

def scaleEdges(edges, S):
    T = getScaleMatrix(S)
    return transformEdges(edges, T)

def projectEdges(edges, k):
    P = getProjectionMatrix(k)
    return transformEdges(edges, P)

def printNodes(edges):
    points = []
    for e in edges:
        for p in e:
            lp = list(p)
            if lp not in points:
                points.append(lp)
    i = 1
    for point in points:
        s = '{0}:\t{1}\t{2}\t{3}\n'.format(i, point[0], point[1], point[2])
        print(s)
        i+=1

class Camera:
    
    def __init__(self, x=0., y=0., z=0., 
                 Rx=0., Ry=0., Rz=0., 
                 k=1., scale=100, width=200, height=200):
        
        self.x = x
        self.y = y
        self.z = z
        self.Rx = Rx
        self.Ry = Ry
        self.Rz = Rz
        self.k = k
        self.scale = scale
        self.width = width
        self.height = height
        
    def getView(self, edges):
        
 
        #m = rotateEdges(m, self.Rx, self.Ry, self.Rz)
        m = transferEdges(edges, -self.x, -self.y, -self.z)
        #m = rotateEdges(m, self.Rx, self.Ry, self.Rz)
        #m = transferEdges(edges, self.x, self.y, self.z)
        m = rotateEdges(m, -self.Rx, -self.Ry, -self.Rz)
        
        m = projectEdges(m, self.k)
        m = scaleEdges(m, self.scale)
        m = transferEdges(m, self.width/2, self.height/2)
        
        return m

#Файл, содержащий фигуру представляет собой список ребер.
#В каждой строке записываются последовательно координаты двух концов ребра.
#1: x1;y1;z1;x2;y2;z2
#2: x1;y1;z1;x2;y2;z2
#...

def load_edges(path):
    f = open(path, 'r')
    edges = []
    for line in f:
        #Удаление символа перевода строки из строки файла
        line = line[:-1]
        numbers = line.split(';')
        #Преобразование чисел в дробный формат
        numbers = list(map(float, numbers))

        p1 = np.array([numbers[0], numbers[1], numbers[2], 1])
        p2 = np.array([numbers[3], numbers[4], numbers[5], 1])
        edges.append([p1, p2])
        
    return edges

def save_edges(edges, path):
    f = open(path, 'w')
    for e in edges:
        line = ''

        for p in e:
            for c in p:
                line = line + "%.4f" % c  + ";"
        
        line = line[:-1]
        f.write(line + '\n')
    f.close()

#Создает окружность радусом r и центральным углом step. 
#Результатом является список ребер.
def generate_circle(r, step):
    x_prev = r
    y_prev = 0
    a = step
    z = 0

    edges = []
    while a <= 360:
        arad = radians(a)
        x = cos(arad) * r
        y = sin(arad) * r

        edges.append([np.array([x_prev, y_prev, z, 1]), np.array([x, y, z, 1])])

        x_prev = x
        y_prev = y
        a = a + step

    return edges

def draw(c, edges):
    for e in edges:
        px1 = e[0][0]
        py1 = e[0][1]
        px2 = e[1][0]
        py2 = e[1][1]
        c.create_line(px1, py1, px2, py2)
      
