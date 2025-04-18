import socket
import sys

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
    if len(sys.argv) != 2:
        print("Usage: python query_client.py <tel.number>")
        sys.exit(1)

    phone_number = sys.argv[1]
    query_history(phone_number)