import math as m
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

dateparser = lambda x: datetime.strptime(x, "%d.%m.%Y")

#Парсинг истории параметров КБД
df = pd.read_csv('dynamic.csv',
                 delimiter=";",
                 decimal=',',
                 skiprows=[0, 1],
                 index_col=[0],
                 parse_dates=[0],
                 date_parser=dateparser)

#Удаление данных о времени закрытия торгов
df = df.drop('tradetime', axis=1)

#Расчет фиксированных параметров КБД ai, bi
k = 1.6
a = [0, 0.6]
for i in range(2, 9):
    a.append(a[i-1] + a[1]*k**(i-1))

b = [a[1]]
for i in range(1, 9):
    b.append(b[i-1]*k)

#Функция G(t) - кривая бескупонной доходности в форме непрерывно начисляемой процентной ставки https://www.moex.com/s2532
#Параметры:
#t - массив array numpy, содержащий сроки погашения, выраженные в годах
#params -  серия bandas, с ключами вида B1, B2, B3, T1, G1, .., G9
#Возвращает массив numpy значений КБД для каждого срока погашения в массиве t

def getG(t, params):   
    B1 = params[0]
    B2 = params[1]
    B3 = params[2]
    T1 = params[3]
    #Получаем список параметров G1-G9
    g_list = list(params[4:])

    #Расчет суммы
    S = 0  
    for i in range(0, 8):
        S = S + g_list[i]*np.exp(-(t-a[i])**2/b[i]**2)

    #Расчет остальных членов выражения
    x1 = (B2+B3)*T1*(1-np.exp(-t/T1))/t
    
    x2 = B3*(np.exp(-t/T1))


    return B1 + \
           x1 - \
           x2 + \
           S
#Y(t) - бескупонная доходность в форме спот-доходности с годовой капитализацией процентов        
#Отображается здесь https://www.moex.com/ru/marketdata/indices/state/g-curve/
def getY(t, params):
    Gt = getG(t, params)
    #Умножаю на 100, потому что хочу получить процентную ставку, а не пункты
    return 100*(np.exp(Gt/10000)-1)

std_t = np.array([0.10, 0.25, 0.5, 0.75, 1, 2, 3, 5, 7, 10, 15, 20, 30])

def getYonDate(year, month, day, t=std_t):
    d = datetime(year, month, day)
    return getY(t, df.loc[d])

def getYinPeriod(y1, m1, d1, y2, m2, d2, t=std_t):
    start = datetime(y1, m1, d1)
    end = datetime(y2, m2, d2)
    df1 = df[start:end]

        
    df1 = df1.sort_index()
    
    buff = []
    new_index = []
    for index, params in df1.iterrows():
        curr_y = getY(t, params)
        buff.append(curr_y)
        new_index.append(index)
    result = pd.DataFrame(buff, columns=std_t, index=new_index)

    return result

def plotYieldCurve(year, month, day, t=std_t):
    #Получение параметров торгов на заданную дату
    date = datetime(year, month, day)
    params = df.loc[ date ]

    Y = getY(t, params)

    #Построение графика и его оформление
    fig, ax = plt.subplots()

    ax.plot(t, Y, linewidth=1.3, color='orange')
    ax.grid(axis='y')

    ax.set_title('График КБД Московской биржи на ' + str(date))
    ax.set_xlabel('Срок до погашения, лет')
    ax.set_ylabel('Значение КБД Московской биржи Y(t)')

    ax.set_xticks(np.arange(0, max(t)+1, 2.5))

    fig.set_figwidth(10)
    fig.set_figheight(5)
    
    plt.show()

def getframe(y1, m1, d1, y2, m2, d2, t=std_t):
    start = datetime(y1, m1, d1)
    end = datetime(y2, m2, d2)
    df1 = df[start:end]

        
    df1 = df1.sort_index()
    buff = []
    for index, params in df1.iterrows():
        curr_y = getY(t, params)
        buff.append(curr_y)
    Y = np.array(buff)
    
    dates = np.array(range(0, len(df1)))
    T, D = np.meshgrid(t, dates)

    return (T, D, Y)

def getHistory(y1, m1, d1, y2, m2, d2, t=std_t):
    start = datetime(y1, m1, d1)
    end = datetime(y2, m2, d2)
    df1 = df[start:end].sort_index()

    Y = []
    for index, params in df1.iterrows():
        Y.append(getY(t, params))

    return Y
        

if __name__ == "__main__":
    plotYieldCurve(2020, 10, 9)
