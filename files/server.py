import socket
import threading

address = ('192.168.100.2', 56789)  # <<----    change your address here !!!

clients = []
nicknames = []

serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.bind(address)
serv_sock.listen()


def serv_client(client):
    while True:
        try:
            buf = str(client.recv(1000), 'utf-8')
            mess = buf.split(':')[1]
            print(mess)
            if mess.lower()[:6] == 'exit()':
                raise 
                break
            elif mess.lower()[:1] == '?':
                serv_resend(bytes('Помощь? )) помоги себе сам %)', 'utf-8'))
            else:
                serv_resend(bytes(buf, 'utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            serv_resend(bytes(f'{nickname} покинул чат!', 'utf-8'))
            nicknames.remove(nickname)
            break


def serv_resend(mess):          # broadcast like
    # print(f'clients {clients} !')
    for client in clients:
        client.send(mess)


def serv_serve():
    client_id = 0
    while True:
        client, addr = serv_sock.accept()
        print(f"Подключен {addr}")

        # запрос и сохранение ника клиента
        client.send(bytes('NICK?', 'utf-8'))
        nickname = str(client.recv(1024), 'utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # вывод и рассылка ника клиента всем подключенным клиентам
        print(f"user: {nickname}")
        serv_resend(bytes(f"{nickname} присоединился к чату!", 'utf-8'))
        client.send(bytes('Подключено к серверу!', 'utf-8'))

        # запуск отдельного потока для обработки сообщений от клиента
        thread = threading.Thread(target=serv_client, args=(client,))
        thread.start()
        client_id += 1


print(serv_sock)
print('Serv started')
serv_serve()
