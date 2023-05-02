import os
import sys

def recursive_search(catalog, pattern):
    prev_catalog = os.getcwd()
    try:
        os.chdir(catalog)
        #Получение данных текущего каталога
        files = os.listdir()
        #Вывести результаты поиска в текущем каталоге
        for file_name in files:
            if pattern in file_name:
                print(os.getcwd() + "\\" + file_name)
        #Для каждого текущего места делаем то же самое   
        for filename in files:
            if os.path.isdir(filename):
                recursive_search(filename, pattern)
        os.chdir(prev_catalog)
    except PermissionError:
        print("***Permission error: " + os.getcwd())    
    
            
catalog = sys.argv[1]
pattern = sys.argv[2]

recursive_search(catalog, pattern)





