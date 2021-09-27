import os, socket, threading, random
from datetime import datetime

udata = {}
log = os.path.dirname((os.path.abspath(__file__))) + '/log.txt'
if not os.path.exists(log):                         #Создаем файл логов
        with open(log, 'w') as f:
            f.write('[%s]:\tLog file started\n'%datetime.now())

def sock8000():
    #ШАГ 3 - получаем от пользователя уникальный идентификатор, записываем его в словарь и отправляем ему уникальный код
    global udata
    sock = socket.socket()
    sock.bind(('', 8000))
    while True:
        sock.listen(50)
        conn, addr = sock.accept()
        while True:
            data = conn.recv(1024)
            if not data: break
            if data.decode('utf-8') in udata.keys():
                conn.send('Your UID already in server data, go 8001'.encode('utf-8'))
            else:
                udata[data.decode('utf-8')] = ''.join(random.choice('0123456789ABCDEF') for _ in range(8))
                conn.send(udata[data.decode('utf-8')].encode('utf-8'))

def sock8001():
    #ШАГ 4 - получаем сообщение и все данные из прошлых пунктов
    global udata
    sock = socket.socket()
    sock.bind(('', 8001))
    while True:
        sock.listen(50)
        conn, addr = sock.accept()
        client_data = []
        while True:
            data = conn.recv(1024)
            if not data or len(client_data)>3: break
            client_data.append(data.decode('utf-8'))
            if len(client_data) == 3:
                if client_data[1] in udata.keys() and udata[client_data[1]] == client_data[2]:
                    #ШАГ 6
                    #Если данные соответствуют тем, что мы сохранили в словарь - записываем сообщение в лог файл
                    conn.send('Your message is logged'.encode('utf-8'))
                    print('[%s]:\t%s'%(datetime.now(),client_data[0]),file=open(log, "a"))
                else:
                    #ШАГ 5
                    #Если нет, то сообщаем пользователю, что его данные не соответствуют сохраненным
                    conn.send('Sorry, incorrect user data =('.encode('utf-8'))
        conn.send('Something gone wrong...'.encode('utf-8'))
            
#ШАГ 1 - создаем два потока, чтобы слушать сразу два порта
thr8000 = threading.Thread(target=sock8000)
thr8001 = threading.Thread(target=sock8001)
thr8000.start()
thr8001.start()