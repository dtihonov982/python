from math import sin, cos, radians
import numpy as np

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


#path = "cube.csv"
#edges = load_edges(path)
#print(edges)

#circle = generate_circle(10, 120)
#save_edges(circle, 'circle.csv')
