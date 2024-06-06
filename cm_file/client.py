import socket
import os

# 服务器的 IP 地址和端口
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

def send_file(filename):
    filesize = os.path.getsize(filename)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())

    with open(filename, "rb") as file:
        while True:
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read: break
            client_socket.sendall(bytes_read)
    
    client_socket.close()

if __name__ == "__main__":
    filename = os.path.join("/home/ec2-user/OJ/cm_file", "sc.c")
    send_file(filename)
