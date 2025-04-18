import socket

def query_history(phone):
    sock = socket.socket()
    sock.connect(('localhost', 5000))
    sock.send(f"HISTORY,{phone}\n".encode())

    while True:
        data = sock.recv(1024).decode()
        if "END" in data:
            break
        print(data.strip())
    sock.close()

if __name__ == "__main__":
    query_history("123456789")