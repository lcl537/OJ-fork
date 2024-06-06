import socket
import sys

def main():
    host = 'localhost'
    port = 12345
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print("Connected to server")
        
        while True:
            message = input("Enter message (type 'exit' to quit): ")
            if message.lower() == 'exit': break
            s.sendall(message.encode())
            data = s.recv(1024)
            if not data: break
            print('Received', repr(data))

if __name__ == '__main__':
    main()
