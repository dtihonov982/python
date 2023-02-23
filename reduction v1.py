##Поиск оптимального дня планирования регулярных платежей.
##
##Планирование постоянных платежей осуществляется на месячный период. Платеж планируется на один день.
##День планирования выбирается исходя из опыта или стандартных условий расчётов.
##
##Цель - повышение точности прогнозирования посредством определения оптимального дня планирования на основании имеющихся данных о платежах.
##
##Данные представляют собой: сумма платежа, точная дата платежа, аналитика (организация, статья движения денежных средств и проч.)
##
##Задачи:
##    
##    1. Дополнить данные недостающими днями, за которые не было платежей
##    2. Вычислить нормализованные суммы, чтобы отклонение суммы не влияло на ошибку планирования.
##    3. Построить потоки.
##    4. Для каждого возможного дня планирования (1 - 31 число месяца) вычислить среднюю абсолютную ошибку (MAD)
##    5. Найти для каждого ключа аналитики день с минимальной погрешностью.

import pandas as pd
from sys import argv
import matplotlib.pyplot as plt

def add_period(df):
    df['Period'] = df['Date'].apply(lambda x: pd.Timestamp(x.year, x.month, 1))

def showMADev(df):
    Y = bestDays['MADev'].values
    X = list(range(1, len(Y)+1))
    plt.plot(X, Y)
    plt.show()

    

if len(argv) == 1:
	input_file = 'test.xlsx'
else:
	input_file = argv[1]
                 
print('Загрузка файла: ' + input_file)
df = pd.read_excel(input_file)

#Список заголовков аналитики, для независимости от используемой аналитики
ahead = list(df.columns)
ahead.remove('Date')
ahead.remove('Sum')

df = df.groupby(ahead+['Date']).sum().reset_index()



###################
#Дополнение дат
print('Выполняется дополнение дат.')

#Минимальная и максимальные даты в списке
#Подразумевается, что для всех ключей аналитики исследуется один период
first = df['Date'].min()
last = df['Date'].max()

#Построение списка всех дат в исследуемых месяцах
start = pd.Timestamp(first.year, first.month, 1)
#Конец месяца, на который приходится последняя дата.
#Получается как начало следующего месяца, минус один день.
end = pd.Timestamp(last.year, last.month+1, 1) + pd.DateOffset(-1)
all_dates = pd.date_range(start, end, freq='D')
all_dates = pd.DataFrame(all_dates, columns=['Date'])

#Добавление периода
add_period(all_dates)
add_period(df)

#Выделение всех ключей аналитики и периодов планирования
keys = df[ahead+['Period']].drop_duplicates()

#Присоединение полного списка дней в рассматриваемых периодах
m = pd.merge(keys, all_dates, on='Period')

###################
#Накопленная сумма
print('Построение потоков.')

#Получение итогов по месяцам
months = df.groupby(ahead+['Period']).sum().reset_index()
months = months.rename(columns={'Sum': 'Total'})

df = df.drop(columns='Period')

#Присоединение сумм к подготовленному списку всех дней
full = pd.merge(m, df, on=ahead+['Date'], how='left')
full = full.fillna(0)

#Присоединение месячных итогов к дополненной таблице
full = pd.merge(full, months, on=ahead+['Period'])
#Вычисление нормализованных сумм
full['Fact'] = full['Sum'] / full['Total']

full = full.drop(columns=['Total'])

#Список уровней, то есть заголовков до даты. Ключи аналитики + Год + Месяц, начиная с нуля
levels = list(range(0, len(ahead)+1))

#Накопленная сумма факта по каждому ключу аналитики и месяцу    
flows = full.groupby(ahead + ['Period', 'Date']).sum().groupby(level=levels).cumsum()
flows = flows.reset_index()

###################
#Перебор дней
print('Перебор дней:')

#Фрейм, содержащий данные о том, сколько в каждом рассматриваемом месяце дней
dayCount = flows.\
       groupby(ahead + ['Period']).\
       count().\
       drop(columns=['Sum', 'Fact']).\
       rename(columns={'Date':'Count'})

#Пустой фрейм, куда будут присоединяться результаты варьирования дня планирования
daysDetail = pd.DataFrame(columns=ahead + ['Period', 'MADev', 'Day'])

#Перебор всех дней - вариантов планирования
maxDay = 31
for day in range(1, maxDay+1):
	#Подразумевается, что по плановый денежный поток имеет вид порога, потому что платеж совершается в один день
	flows['Plan'] = flows['Date'].apply(lambda x: 1 if x.day >= day else 0)
	#Абсолютной отклонение для последующего расчета MADev
	flows['Deviation'] = abs(flows['Fact'] - flows['Plan'])

	#Расчёт MADev по дням для данного варианта планирования
	g = flows.groupby(ahead+['Period']).sum()
	#???
	m = pd.merge(g, dayCount, left_index=True, right_index=True)
	m['MADev'] = m['Deviation'] / m['Count']
	m['Day'] = day

	m = m.drop(columns=['Sum', 'Fact', 'Plan', 'Deviation', 'Count']).reset_index()

	daysDetail = pd.concat([daysDetail, m])
	print('{}/{}'.format(day, maxDay))

flows = flows.drop(columns=['Plan', 'Deviation'])

###################
#Поиск дней с минимальной средней абсолютной ошибкой.

daysWithoutPeriods = daysDetail.groupby(ahead+['Day']).mean().reset_index() 

minimals =  daysWithoutPeriods\
       .groupby(ahead)\
       .idxmin()
  
indexOfMin = minimals['MADev'].values
bestDays = daysWithoutPeriods\
           .iloc[indexOfMin]\
           .sort_values('MADev')\
           .reset_index()\
           .drop(columns='index')

if len(argv) == 3:
	print('Сохранение результата в файл: ' + argv[2])
	bestDays.to_excel(argv[2])
	
print('Готово.')

