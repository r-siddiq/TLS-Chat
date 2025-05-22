#!env python

"""Chat server for CST311 Programming Assignment 4"""
__author__ = "Team 9"
__credits__ = [
    "Victor Gomez",
    "Rahim Siddiq",
    "Arielle Lauper"
]

import socket as s
import threading
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
server_port = 12000
server_host = '10.0.1.2'  # Updated server IP address
clients = {}  # Store client sockets and their names

def connection_handler(client_name):
    connection_socket = clients[client_name]

    try:
        while True:
            # Receive message from the client
            message = connection_socket.recv(1024)
            if not message:
                break
            message_decoded = message.decode()
            log.info(f"Received message from {client_name}: {message_decoded}")
            # If the client sends "bye", notify other clients and close the connection
            if message_decoded.lower() == "bye":
                log.info(f"{client_name} has left the chat.")
                broadcast_message(f"{client_name} has left the chat.", exclude=client_name)
                break
            # Broadcast the message to other clients
            broadcast_message(f"Message from {client_name}: {message_decoded}", exclude=client_name)
    except Exception as e:
        log.error(f"Error handling client {client_name}: {e}")
    finally:
        # Close the connection socket and remove the client
        log.info(f"{client_name} disconnected.")
        connection_socket.close()
        if client_name in clients:
            del clients[client_name]

def broadcast_message(message, exclude=None):
    """Broadcast a message to all clients except the excluded one."""
    for name, client_socket in clients.items():
        if name != exclude:
            try:
                client_socket.send(message.encode())
            except Exception as e:
                log.error(f"Failed to send message to {name}: {e}")

def main():
    # Create a TCP socket
    server_socket = s.socket(s.AF_INET, s.SOCK_STREAM)
    # Bind the socket to the server IP and port
    server_socket.bind((server_host, server_port))
    # Listen for incoming connections (queue up to 3 clients)
    server_socket.listen(3)
    log.info(f"The server is ready to receive on IP {server_host} and port {server_port}")

    try:
        # Accept connection from Client X
        connection_socket_x, address_x = server_socket.accept()
        log.info(f"Client X connected from {address_x}")
        clients["Client X"] = connection_socket_x

        # Accept connection from Client Y
        connection_socket_y, address_y = server_socket.accept()
        log.info(f"Client Y connected from {address_y}")
        clients["Client Y"] = connection_socket_y

        # Accept connection from Client Z
        connection_socket_z, address_z = server_socket.accept()
        log.info(f"Client Z connected from {address_z}")
        clients["Client Z"] = connection_socket_z

        # Start threads to handle all clients
        threading.Thread(target=connection_handler, args=("Client X",)).start()
        threading.Thread(target=connection_handler, args=("Client Y",)).start()
        threading.Thread(target=connection_handler, args=("Client Z",)).start()
    except Exception as e:
        log.error(f"Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
