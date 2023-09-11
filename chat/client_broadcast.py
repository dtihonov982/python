#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading
from time import sleep

sock = socket.socket()

print('Подключаюсь к серверу...')
connected = False
while True:
    try:
        sock.connect(('localhost', 9090))
        connected = True
        break
    except:
        pass

print('Подключение установлено.')

def listening():
    global connected
    try:
        while True:
            data = sock.recv(1024)
            print(data.decode())
    except ConnectionResetError:
        connected = False
        print('Соединение разорвано.')
        return
    except:
        connected = False
        print('Что-то пошло не так.')
        return

def sending():
    while True:
        text = input('> ')
        if connected:
            sock.send(text.encode())
        else:
            return

threading.Thread(target=listening).start()
threading.Thread(target=sending).start()
