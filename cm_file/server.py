import socket
import os

SERVER_HOST = '15.164.222.83'
SERVER_PORT = 443
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(5)
print(f"[*] 服务器正在监听 {SERVER_HOST}:{SERVER_PORT}")

def save_file(file_data, filename):
    save_path = os.path.join(".", filename)
    
    # 确保保存目录存在
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    
    # 将文件内容写入指定文件
    with open(save_path, "wb") as file:
        file.write(file_data)
    return save_path

while True:
    # 接受客户端连接
    client_socket, client_address = server_socket.accept()
    print(f"[+] {client_address} 已连接.")
    
    # 接收文件信息
    received = client_socket.recv(BUFFER_SIZE).decode()
    filename, filesize = received.split(SEPARATOR)
    filename = os.path.basename(filename)
    filesize = int(filesize)

    # 接收文件内容
    file_data = b""
    while True:
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read: break
        file_data += bytes_read
    
    # 保存文件并打印内容
    save_filename = "received_code" + os.path.splitext(filename)[1]
    save_path = save_file(file_data, save_filename)

    print(f"[+] 文件已保存: {save_path}")
    print("\nCode content\n")
    with open(save_path, "r") as file:
        print(file.read())
    
    # 关闭客户端连接
    client_socket.close()
