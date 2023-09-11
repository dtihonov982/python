import os
import sys

def recursive_search(catalog, pattern):
    prev_catalog = os.getcwd()
    try:
        os.chdir(catalog)
        cwd = os.getcwd()
        #Получение данных текущего каталога
        files = os.listdir()
        #Вывести результаты поиска в текущем каталоге
        for file_name in files:
            if pattern in file_name:
                full_path = os.path.join(cwd, file_name);
                print(full_path)
        #Для каждого текущего места делаем то же самое   
        for filename in files:
            if os.path.isdir(filename):
                recursive_search(filename, pattern)
        os.chdir(prev_catalog)
    except PermissionError:
        print("***Permission error: " + os.getcwd())    
    
if len(sys.argv) == 3:        
    recursive_search(sys.argv[1], sys.argv[2])
else:
    print("find [where] [what]")







