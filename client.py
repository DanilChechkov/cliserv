import socket

print('\nCONNECTION WITH :8000\n')

#ШАГ 2 - пользователь выбирает для себя уникальный идентификатор
uid = str(input('Choose UID:\t'))
sock = socket.socket()
#ШАГ 3 - клиент подключается к серверу к порту 8000 и передает свой уникальный идентификатор
sock.connect(('localhost', 8000))
sock.send(uid.encode('utf-8'))
#ШАГ 3 - Клиент получает от сервера уникальный код
data = sock.recv(1024)
sock.close()
print('Security key:\t' + data.decode('utf-8'))
#ШАГ 4 - Клиент подключается к серверу к порту 8001
print('\nCONNECTION WITH:8001\n')
sock = socket.socket()
sock.connect(('localhost', 8001))
#ШАГ 4 - передает произвольное текстовое сообщение
message = str(input('Your message:\t'))
sock.send(message.encode('utf-8'))
#ШАГ 4 - Передает свой уникальный идентификатор
uid = str(input('Enter UID:\t'))
sock.send(uid.encode('utf-8'))
#ШАГ 4 - Передает свой код полученный на шаге 3
secret_key = str(input('Enter secret key:\t'))
sock.send(secret_key.encode('utf-8'))
data = sock.recv(1024)
#ШАГ 5 - Ждем ответ от сервера
print('Server answer:\t' + data.decode('utf-8'))
sock.close()