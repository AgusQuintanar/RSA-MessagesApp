#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import datetime
import rsa

class Client():
    def __init__(self):
        HOST = '127.0.0.1'
        PORT = 33000
        self.BUFSIZ = 1024
        ADDR = (HOST, PORT)
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)
        self.available_messages = []
        self.PUBLIC_KEY, self.PRIVATE_KEY = rsa.generate_keys()

    def receive(self):
        """ Fetches encrypted messages from server, and decrypts it """
        while True:
            try:
                msg_received = self.client_socket.recv(self.BUFSIZ).decode("utf8").split("<!||||!>")
                if len(msg_received) > 1:
                    user, encrypted_message = msg_received
                    print("received message:", encrypted_message)
                    message = rsa.decrypt(encrypted_message, self.PUBLIC_KEY[0], self.PRIVATE_KEY)
                    print(f"user: {user}, message: {message}")
                    self.available_messages.append((user, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"), message))
            except OSError:  # Possibly client has left the chat.
                break


    def send(self, message, event=None):
        """ sends message to server for encryption and broadcast """  
        self.client_socket.send(bytes(message, "utf8"))

    def send_public_key(self):
        """ sends user's public key """
        self.send(str(self.PUBLIC_KEY[0]) + "," + str(self.PUBLIC_KEY[1]))

    def on_closing(self, event=None):
        """This function is to be called when the window is closed."""
        self.send("{quit}")
