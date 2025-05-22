#!env python

"""Chat client for CST311 Programming Assignment 4"""
__author__ = "Team 9"
__credits__ = [
    "Victor Gomez",
    "Rahim Siddiq",
    "Arielle Lauper"
]

# Import statements
import socket as s
import threading
import logging

# Configure logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# Set global variables
server_name = '10.0.1.2'  # Updated server IP address
server_port = 12000

# Listener for incoming messages
def message_listener(socket):
    while True:
        try:
            # Read response from server
            server_response = socket.recv(1024)
            # If there is a response
            if server_response:
                # Decode server response from UTF-8 bytestream
                server_response_decoded = server_response.decode()
                # Print output from server
                print(server_response_decoded)
            # Exit loop if no response or exception
            else:
                break
        except Exception as e:
            log.exception(e)
            break

def main():
    # Create socket
    client_socket = s.socket(s.AF_INET, s.SOCK_STREAM)

    try:
        # Establish TCP connection
        client_socket.connect((server_name, server_port))
    except Exception as e:
        log.exception(e)
        log.error("***Advice:***")
        if isinstance(e, s.gaierror):
            log.error("\tCheck that server_name and server_port are set correctly.")
        elif isinstance(e, ConnectionRefusedError):
            log.error("\tCheck that server is running and the address is correct")
        else:
            log.error("\tNo specific advice, please contact teaching staff and include text of error and code.")
        exit(8)

    print('Welcome to the chat! To send a message, type a message and click enter.')
    # Thread to listen for incoming messages
    t1 = threading.Thread(target=message_listener, args=(client_socket,))
    t1.daemon = True  # Mark the listener thread as a daemon thread
    t1.start()

    # Get input from user
    while True:
        user_input = input()

        # Wrap in a try-finally to ensure the socket is properly closed regardless of errors
        try:
            # Send data across socket to server
            client_socket.send(user_input.encode())
        except Exception as e:  # Ensure socket closes if exception
            log.exception(e)
            client_socket.close()
        # Close connection if user inputs "bye"
        if user_input.lower() == "bye":
            break
    # Close socket when client leaves
    client_socket.close()

if __name__ == "__main__":
    main()
