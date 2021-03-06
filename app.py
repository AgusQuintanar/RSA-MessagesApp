import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from chat import Chat
from client import Client
from threading import Thread
from socket import AF_INET, socket, SOCK_STREAM
from time import sleep


COLOUR_LIGHT_BACKGROUND_1 = "#fff"
COLOUR_LIGHT_BACKGROUND_2 = "#f2f3f5"
COLOUR_LIGHT_BACKGROUND_3 = "#e3e5e8"

COLOUR_LIGHT_TEXT = "#aaa"

COLOUR_BUTTON_NORMAL = "#5fba7d"
COLOUR_BUTTON_ACTIVE = "#58c77c"
COLOUR_BUTTON_PRESSED = "#44e378"


class Messenger(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        #####################################  WINDOW #########################################
        self.geometry("1200x500")
        self.minsize(800, 500)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title("AlphaChat v1.0 by Agus Quintanar")
        ########################################################################################

        ####################################### STYLE ##########################################

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Messages.TFrame", background=COLOUR_LIGHT_BACKGROUND_3)

        style.configure("MessagesOwner.TFrame", background="#25D366")

        style.configure("Controls.TFrame", background=COLOUR_LIGHT_BACKGROUND_2)

        style.configure("SendButton.TButton", borderwidth=0, background=COLOUR_BUTTON_NORMAL)
        style.map(
            "SendButton.TButton",
            background=[("pressed", COLOUR_BUTTON_PRESSED), ("active", COLOUR_BUTTON_ACTIVE)],
        )

        style.configure(
            "FetchButton.TButton", background=COLOUR_LIGHT_BACKGROUND_1, borderwidth=0
        )

        style.configure(
            "Time.TLabel",
            padding=5,
            background=COLOUR_LIGHT_BACKGROUND_1,
            foreground=COLOUR_LIGHT_TEXT,
            font=8
        )

        style.configure(
            "TimeOwner.TLabel",
            padding=5,
            background="#4B9EFF",
            foreground=COLOUR_LIGHT_BACKGROUND_1,
            font=8
        )

        style.configure("Avatar.TLabel", background=COLOUR_LIGHT_BACKGROUND_3, padding=5)
        style.configure("Message.TLabel", background=COLOUR_LIGHT_BACKGROUND_2, padding=5)
        style.configure("MessageOwner.TLabel", background="#71B3FF")
        #############################################################################################

        ##################################### CHAT  #################################################
        self.chat_frame = Chat(
            self,
            background=COLOUR_LIGHT_BACKGROUND_3,
            style="Messages.TFrame"
        )

        self.chat_frame.grid(row=0, column=0, sticky="NSEW")
        self.chat_frame.client.send_public_key()
        username = input("Enter your username: ")
        self.chat_frame.client.send(username)
        self.chat_frame.user = username
        self.protocol("WM_DELETE_WINDOW", self.chat_frame.client.on_closing)

        ###############################################################################################

      
if __name__ == '__main__':
    root = Messenger()
    receive_thread = Thread(target=root.chat_frame.client.receive)
    receive_thread.start()
    root.mainloop()  

