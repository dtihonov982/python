#Инструменты поиска на компьютере файловых информационных баз 1С: Предприятие
#Можно посмотреть так же, какие базы 1. Незарегистрированы в приложении 2. Зарегистрированы, но реально удалены.

import re, os
from os.path import isdir, isfile

##Можно загрузить список зарегистрированных ИБ с помощью процедуры load_ilist
##из стандартного файла вида *.v8i и сравнить со списком реально существующих. 
def load_ilist(v8i_file):
    pattern = re.compile(r'File="(.+)"')
    file = open(v8i_file, 'r')
    result = []
    for line in file:
        m = pattern.search(line)
        if m:
            result.append(m.group(1))
    return result

#Проверяет, является ли каталог информационной базой
def is_infobase(directory):
    p = re.compile('.*\.1[cC][Dd]')
    #print(directory)
    for i in os.listdir(directory):
        if p.search(i):
            return True
    return False

#Возвращает список папок, содержащихся в каталоге top
def dirs_list(top):
    _alllist = os.listdir(top)
    alllist = map(lambda x: os.path.join(top, x), _alllist)
    res = filter(isdir, alllist)
    return list(res)


#search_infobases - рекурсивно ищет информационные базы 1С, начиная с каталога top.
#
#В процессе поиска попадаются громоздкие папки, наверняка не содержащие и.б. 1С, например C:\Windows.
#Такие каталоги можно исключить из поиска, добавив их в список pass_list.
#
#Возвращает кортеж (result, errors), где result - список найденных информационных баз,
#errors - список папок в которых по каким-либо причинам невозможен поиск.
def search_infobases(top, pass_list=[]):
    queue = dirs_list(top)
    result = []
    errors = []
    for d in queue:
        
        if d in pass_list:
            continue
        
        try:
            if is_infobase(d):
                result.append(d)
            else:
                queue.extend(dirs_list(d))
        except:
            errors.append('###Неизвестная ошибка. Каталог ' + d)
            
    return (result, errors)           

def print_list(l):
    counter = 1
    for el in l:
        print('({0}) {1}'.format(counter, el))
        counter += 1


def analisys(real, registred):
    _real = set(real)
    _reg = set(registred)

    correct = _real & _reg
    unreg = _real - _reg
    void = _reg - _real

    return {'correct':correct, 'unregistred':unreg, 'void':void}

def main():
    main_dir = input('Введите имя директории, в которой будет вестись поиск, например, С:\\\n> ')

    try:
        result, errors = search_infobases(main_dir, std_pass_list)

        print_list(result)

        key = input('Показать ошибки?(Y/N)')
        if key == 'Y':
            print_list(errors)
    except:
        print('Неизвестная ошибка')    

std_pass_list = [r'C:\Windows', r'C:\Program Files', r'C:\Program Files (x86)', r'C:\$Recycle.Bin']

if __name__ == '__main__':
    main()
