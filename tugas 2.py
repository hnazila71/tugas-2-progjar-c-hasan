from socket import *
import socket
import threading
import logging
import time
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define the client processing class
class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                # Receive data from the client
                data = self.connection.recv(1024)
                if data:
                    # Decode the received data
                    data_str = data.decode('utf-8').strip()
                    logging.info(f"Received data: {data_str}")
                    
                    # Check if the request starts with "TIME" and ends with CR LF
                    if data_str == "TIME":
                        # Get the current time
                        current_time = time.strftime("%H:%M:%S")
                        response = f"JAM {current_time}\r\n"
                        # Send the response to the client
                        self.connection.sendall(response.encode('utf-8'))
                    # Check if the request is "QUIT" and ends with CR LF
                    elif data_str == "QUIT":
                        break
                    else:
                        # Send an error response if the request is invalid
                        self.connection.sendall("Invalid request\r\n".encode('utf-8'))
                else:
                    break
            except:
                break
        self.connection.close()

# Define the server class
class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))
        self.my_socket.listen(5)
        logging.info("Server started on port 45000")
        
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.info(f"Connection from {self.client_address}")
            
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)

# Main function to start the server
def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
