from tkinter import *
import customtkinter
import socket
import threading
import pickle

HOST = socket.gethostbyname('localhost')
PORT = 9999

root = customtkinter.CTk()
root.geometry('1000x550')
root.resizable(False, False)


def appClient():
    #! INTERFACE GRAFICA
    chat_frame = customtkinter.CTkFrame(master=root,
                                        width=850, height=550,
                                        fg_color='#C0BFC0')
    chat_frame.grid(row=0, column=1)

    lateral_bar = customtkinter.CTkFrame(master=root,
                                        width=150, height=550,
                                        fg_color='#161616')
    lateral_bar.grid(row=0, column=0)

    #! PYTHON SOCKET
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((HOST, PORT))
        print('Conectado ao server com sucesso!')
    except socket.error as e:
        print(f'Erro ao se conectar: {e}')
        client.close()
        client.exit()

    username = input('\nUsuário: ')
    print(f'{username} conectado!')

    # ^Enviando username serializado para o  server
    username_serialized = pickle.dumps(username)
    client.send(username_serialized)

    dialog_bar = customtkinter.CTkEntry(master=chat_frame,
                                        font=('Inter', 15),
                                        width=700, height=30,
                                        fg_color='white',
                                        placeholder_text="Digite uma mensagem... ",
                                        text_color='black',bg_color='#C0BFC0')
    dialog_bar.place(x=20, y=500)

    def enviarMsg(client, username):  # ! TRY??
        try:
            msg = dialog_bar.get()
            client.send(f'{username}: {msg}'.encode('utf-8'))
            dialog_bar.delete(0, END)
        except:
            print('Erro ao enviar mensagem!!')
            client.close()
            client.exit()
            return

    btn_enviar = customtkinter.CTkButton(master=root,
                                        width=5, height=15,
                                        bg_color='#C0BFC0', text='Enviar',
                                        command=lambda: enviarMsg(client, username))
    btn_enviar.place(x=900, y=505)

    def recvMsg(client):
        while True:
            try:
                msg = client.recv(1048).decode('utf-8')
                print(msg + '\n')
            except:
                print('Erro!')
                client.exit()
                break

    th_two = threading.Thread(target=recvMsg, args=[client])
    th_one = threading.Thread(target=enviarMsg, args=[client, username])
    th_two.start()
    th_one.start()

    root.title(username)
    root.mainloop()


if __name__ == "__main__":
    appClient()
