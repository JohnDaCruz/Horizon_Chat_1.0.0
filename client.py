from tkinter import *
import customtkinter
import threading
import socket

root = customtkinter.CTk()
root.geometry('1000x550')
root.resizable(False, False)
root.title('Horizon chat')

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect(('localhost', 7777))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    username = input('Usuário> ')
    print('\nConectado')

    thread1 = threading.Thread(target=receiveMessages, args=[client])
    thread2 = threading.Thread(target=sendMessages, args=[client, username])

    thread1.start()
    thread2.start()

def receiveMessages(client):
    while True:
        try:
            msg = client.recv(2048).decode('utf-8')
            print(msg+'\n')
        except:
            print('\nNão foi possível permanecer conectado no servidor!\n')
            print('Pressione <Enter> Para continuar...')
            client.close()
            break
        
def sendMessages(client, username):
    btn_enviar = customtkinter.CTkButton(master=root,
                                        width=5, height=15,
                                        bg_color='#C0BFC0', text='Enviar',
                                        command=lambda: sendMessages(client, username))
    btn_enviar.place(x=900, y=505)
    try:
        msg = dialog_bar.get()
        client.send(f'<{username}> {msg}'.encode('utf-8'))
        dialog_bar.delete(0,END)
    except:
        return     

chat_frame = customtkinter.CTkFrame(master=root,
                                    width=850,
                                    height=550,
                                    fg_color='#C0BFC0')
chat_frame.grid(row=0, column=1)

lateral_bar = customtkinter.CTkFrame(master=root,
                                    width=150,
                                    height=550,
                                    fg_color='#161616')
lateral_bar.grid(row=0, column=0)

dialog_bar = customtkinter.CTkEntry(master=chat_frame,
                                        font=('Inter', 15),
                                        width=700, height=30,
                                        fg_color='white',
                                        placeholder_text="Digite uma mensagem... ",
                                        text_color='black',bg_color='#C0BFC0')
dialog_bar.place(x=20, y=500)

main()
root.mainloop()