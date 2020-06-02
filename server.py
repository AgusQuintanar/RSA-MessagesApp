#!/usr/bin/env python3

import rsa
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    CLIENT_PUBLIC_KEY = client.recv(BUFSIZ).decode("utf8").split(",")
    name = client.recv(BUFSIZ).decode("utf8")
    print("incoming PK:", CLIENT_PUBLIC_KEY, "type", type(CLIENT_PUBLIC_KEY), "name", name)
    clients[client] = (name, CLIENT_PUBLIC_KEY)

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name+"<!||||!>")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        user, PUBLIC_KEY = clients[sock]
        print("PUBLIC KEY:", PUBLIC_KEY)
        print("message to encrypt:", msg.decode("utf8"))
        encrypted_msg = rsa.encrypt(msg.decode("utf8"), PUBLIC_KEY)
        print("message to decrypt:", encrypted_msg)
        sock.send(bytes(prefix, "utf8")+bytes(encrypted_msg, "utf8"))


############################## SERVER CONFIGURATION ########################################
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
#############################################################################################

if __name__ == "__main__":
    SERVER.listen(8) #MAX CAPACITY
    print("Server Initialized")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()