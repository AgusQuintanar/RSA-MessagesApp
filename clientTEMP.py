import socket
import select
import errno
from time import sleep


class Client():
    def __init__(self, chat):
        self.HEADER_LENGTH = 10

        IP = "127.0.0.1"
        PORT = 1234
        self.my_username = input("Username: ")

        self.chat = chat

        # Create a socket
        # socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
        # socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to a given ip and port
        self.client_socket.connect((IP, PORT))

        # Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
        self.client_socket.setblocking(False)

        # Prepare username and header and send them
        # We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
        username = self.my_username.encode('utf-8')
        username_header = f"{len(username):<{self.HEADER_LENGTH}}".encode('utf-8')
        self.client_socket.send(username_header + username)

        self.message = ""
        self.is_message_sent = False

        self.available_messages = []

    
    def fetch_available_messages(self):
        try:
            # Now we want to loop over received messages (there might be more than one) and print them
            while True:
                
                # Receive our "header" containing username length, it's size is defined and constant
                username_header = client_socket.recv(HEADER_LENGTH)

                # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
                if not len(username_header):
                    print('Connection closed by the server')
                    exit()

                # Convert header to int value
                username_length = int(username_header.decode('utf-8').strip())

                # Receive and decode username
                username = client_socket.recv(username_length).decode('utf-8')

                # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
                message_header = client_socket.recv(HEADER_LENGTH)
                message_length = int(message_header.decode('utf-8').strip())
                message = client_socket.recv(message_length).decode('utf-8')

                print("tratando de hacer fetch")


                # Print message
                print(f'{username} > {message}')

                self.available_messages.append((username, message))

        except IOError as e:
            # We just did not receive anything
            pass

        except Exception as e:
            # Any other exception - something happened, exit
            pass


    def listen(self):
        while True:

             # If message is not empty - send it
            if len(self.message) > 0 and self.is_message_sent:
                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                self.message = self.message.encode('utf-8')
                message_header = f"{len(self.message):<{self.HEADER_LENGTH}}".encode('utf-8')
                self.client_socket.send(message_header + self.message)
                self.is_message_sent = False
                self.message = ""
            else:
                self.fetch_available_messages()

           

            sleep(.0002)

    

# c = Client()
# c.initialize_communication()