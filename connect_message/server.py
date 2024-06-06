import socket

def main():
    host = 'localhost'
    port = 12345
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print("Server is listening on port", port)
        
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    mes = data.decode('utf-8')
                    print(mes)
                    conn.sendall(data)  # Echo the received data back to the client

if __name__ == '__main__':
    main()
