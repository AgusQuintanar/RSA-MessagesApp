#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import datetime

class Client():
    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 33000
    
        self.BUFSIZ = 1024
        ADDR = (HOST, PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)

        self.available_messages = []

    def receive(self):
        while True:
            try:
                msg=self.client_socket.recv(self.BUFSIZ).decode("utf8")
                print("mensaje enviado:", msg)
                user, message = msg.split("<!||||!>")
                print(f"user: {user}, message: {message}")
                self.available_messages.append((user, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), message))
            except OSError:  # Possibly client has left the chat.
                break


    def send(self, message, event=None):  
        self.client_socket.send(bytes(message, "utf8"))
