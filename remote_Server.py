import socket
import threading
from pynput import keyboard, mouse
from screeninfo import get_monitors

# Variables
SERVER = None
IP_ADDRESS = "192.168.0.111"  # Replace with your actual IP address
PORT = 8000

# Get screen size
def getDeviceSize():
    monitor = get_monitors()[0]
    return monitor.width, monitor.height

# Setup server
def setup():
    global SERVER
    global IP_ADDRESS
    global PORT

    try:
        SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SERVER.bind((IP_ADDRESS, PORT))
        SERVER.listen(100)  # Listen for a maximum of 100 connections
        print("Server started. Waiting for connections...")
    except Exception as e:
        print("Server setup failed:", str(e))

# Accept incoming connections
def acceptConnections():
    while True:
        client_socket, client_address = SERVER.accept()
        print(f"New connection from {client_address[0]}:{client_address[1]}")

        # Create a separate thread for each client request
        client_thread = threading.Thread(target=recvMessage, args=(client_socket,))
        client_thread.start()

# Receive and handle client messages
def recvMessage(client_socket):
    global keyboard

    while True:
        try:
            message = client_socket.recv(4096).decode('utf-8')
            if message == "pressed":
                keyboard.press(keyboard.Key.space)
            elif message == "released":
                keyboard.release(keyboard.Key.space)
        except Exception as e:
            print("Error handling client message:", str(e))
            break

# Start the server
def startServer():
    setup_thread = threading.Thread(target=setup)
    setup_thread.start()

    accept_thread = threading.Thread(target=acceptConnections)
    accept_thread.start()

# Main execution
if __name__ == '__main__':
    # Initialize the keyboard controller
    keyboard = keyboard.Controller()

    # Start the server
    startServer()
