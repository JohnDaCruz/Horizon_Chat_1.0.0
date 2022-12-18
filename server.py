import socket
import threading
import pickle

HOST = socket.gethostbyname('localhost')
PORT = 9999
clients = []


def appServer():

    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f'Server listening on: {HOST},{PORT}')

    except socket.error as e:
        print(f'Erro ao abrir server: {e}')

    server.bind((HOST, PORT))

    server.listen(10)

    # Escutando client
    usernames_list = []
    while True:
        client, addr = server.accept()
        clients.append(client)
        print(client, addr)

        #^ Capturando o username de client 
        username_from_client = client.recv(1048).decode('utf-8')
        usernames_list.append(username_from_client)
        print(usernames_list)

        th_broadcast = threading.Thread(target=tratandoMsg, args=[client])
        th_broadcast.start()

def tratandoMsg(client):
    while True:
        try:
            msg = client.recv(2048)
            broadcast(msg, client)
        except:
            removeClient(client)
            break


def broadcast(msg, client):
    for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                print("Error sending message")
                removeClient()


def removeClient(client):
    clients.remove(client)


appServer()