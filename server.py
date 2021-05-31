from socket import AF_INET,socket,SOCK_STREAM
from threading import Thread

HOST='127.0.0.1'
PORT=55000
SIZE=2048
ADDR=(HOST,PORT)

SERVER=socket(AF_INET,SOCK_STREAM)
SERVER.bind(ADDR)

clients={}
addresses={}

def accept_incoming_connections():
    while True:
        client,client_address=SERVER.accept()
        addresses[client]=client_address
        Thread(target=handle_client,args=(client,)).start()

def handle_client(client):
    name=client.recv(SIZE).decode("utf8") 

    msg=f"{name} has joined the chat!"
    broadcast(bytes(msg,"utf8"))

    clients[client]=name

    while True:
        msg=client.recv(SIZE)   #receives msg from client and sends to broadcast func
        if msg!=bytes("{quit}", "utf8"):
            broadcast(msg,name+" : ")
        else:   #means the user has entered {quit}
            client.send(bytes("{quit}","utf8"))
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} has left the chat.","utf8"))
            break

def broadcast(msg,prefix=""):  # prefix is for name identification.
    #Broadcasts a message to all the clients.
    for sock in clients:
        sock.send(bytes(prefix,"utf8")+msg)

if __name__=="__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD=Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()