import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

SCREEN_SIZE_TO_MESSAGE_WIDTH = {
    1100: 900,
    950: 700,
    750: 550
}


class MessageWindow(tk.Canvas):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs, highlightthickness=0)

        self.messages_frame = ttk.Frame(container, style="Messages.TFrame")
        self.messages_frame.columnconfigure(0, weight=1)

        self.scrollable_window = self.create_window((0, 0), window=self.messages_frame, anchor="nw", width=self.winfo_width())

        def configure_scroll_region(event):
            self.configure(scrollregion=self.bbox("all"))
        
        def configure_window_size(event):
            self.itemconfig(self.scrollable_window, width=self.winfo_width())

        self.bind("<Configure>", configure_window_size)
        self.messages_frame.bind("<Configure>", configure_scroll_region)
        self.bind_all("<MouseWheel>", self._on_mousewheel)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.yview)
        scrollbar.grid(row=0, column=1, sticky="NS")

        self.configure(yscrollcommand=scrollbar.set)
        self.yview_moveto(1.0)
    
    def _on_mousewheel(self, event):
        self.yview_scroll(-int(event.delta/120), "units")

    def update_message_widgets(self, messages, message_labels, current_user):
        existing_labels = [
            (user["text"], time["text"], message["text"]) for user, time, message in message_labels
        ]


        for message in messages:

            if (message[0], message[1], message[2]) not in existing_labels:
                self._create_message_container(message[0], message[2], message[1], message_labels, current_user)
    
    def _create_message_container(self, message_user, message_content, message_time, message_labels, current_user):
        if current_user == message_user:
            container = ttk.Frame(self.messages_frame, style="MessagesOwner.TFrame")
            container.columnconfigure(1, weight=1)
            container.grid(sticky="EW", padx=(int(self.winfo_screenmmwidth()/2), 10), pady=10)
        else: 
            container = ttk.Frame(self.messages_frame, style="Messages.TFrame")
            container.columnconfigure(1, weight=1)
            container.grid(sticky="EW", padx=(10, int(self.winfo_screenmmwidth()/2)), pady=10)
        

        def reconfigure_message_labels(event):
            closest_break_point = min(SCREEN_SIZE_TO_MESSAGE_WIDTH.keys(), key=lambda b: abs(b - container.winfo_width()))
            for label, _, _ in message_labels:
                if label.winfo_width() < closest_break_point:
                    label.configure(wraplength=SCREEN_SIZE_TO_MESSAGE_WIDTH[closest_break_point])
            self.messages_frame.update()

        container.bind("<Configure>", reconfigure_message_labels)
        self._create_message_bubble(container, message_user, message_content, message_time, message_labels, current_user)
    
    def _create_message_bubble(self, container, message_user, message_content, message_time, message_labels, current_user):

        if current_user == message_user:
            s_top = "TimeOwner.TLabel"
            s_message = "MessageOwner.TLabel"
        else:
            s_top = "Time.TLabel"
            s_message = "Message.TLabel"

        user_label = ttk.Label(
            container,
            text=message_user,
            style=s_top
        )

        user_label.grid(row=0, column=1, sticky="NEW")

        time_label = ttk.Label(
            container,
            text=message_time,
            style=s_top,
            justify="right",
            anchor="e",
        )

        time_label.grid(row=0, column=2, sticky="NEW")

        message_label = ttk.Label(
            container,
            text=message_content,
            wraplength=800,
            justify="left",
            anchor="w",
            style=s_message
        )

        message_label.grid(row=1, column=1, sticky="NEW", columnspan=2)

        message_labels.append((user_label, time_label, message_label))