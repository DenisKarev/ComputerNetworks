import socket
import threading

nickname = input("Enter your nickname: ")
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

addr = ('158.160.113.26', 56789)


client.connect(addr)
# message = f"{nickname}:{input('Message to send: ')}"
# client.send(bytes(message + "\n", "utf-8"))
# received = str(client.recv(1024), "utf-8")

# print(f"Sent:     {message}")
# print(f"Received: {received}")

def receive():
    while True:
        try:
            message = str(client.recv(1024), "utf-8")
            if message == 'NICK?':
                client.send(bytes(nickname, 'utf-8'))
            else:
                # message = f'{nickname}: {message}'
                print(f'{message}')
        except:
            print('err')
            client.close()
            break


def write():
    while True:
        message = f"{nickname}:{input('')}"
        client.send(bytes(message + "\n", "utf-8"))


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
