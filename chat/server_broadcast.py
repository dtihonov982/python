#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import threading

sock = socket.socket()
sock.bind(('', 9090))
sock.listen(3)

#Список всех подключенных клиентов
all_conns = []

def Reciever(conn, addr):
    global all_conn
    while True:
        try:
            data = conn.recv(1024)
        except:
            print('Клиент отключен. ' + str(addr))
            conn.close()
            all_conns.remove(conn)    
            return
             
        message_text = 'Клиент {}:{}> {}'.format(addr[0], addr[1], data.decode())
        broadcast(message_text, conn)
        
def broadcast(message, sender):
    for c in all_conns:
        if c != sender:
            c.send(message.encode())
    
while True:            
    print('Жду подключения...')
    host = sock.accept()
    all_conns.append(host[0])
    
    print('Подключен клиент. ' + str(host[1]))
    
    #Запуск потока обслуживания пользователя
    threading.Thread(target=Reciever, args=host).start()
