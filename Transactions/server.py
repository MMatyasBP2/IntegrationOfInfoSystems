import socket
import threading
import uuid
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://matyika123456:H4FdxLQcNMOQvoBT@transactiondb.fcusdo6.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['TransactionDB']
transactions = db['Transactions']

HOST = 'localhost'
PORT = 5000
ALLOWED_AMOUNTS = {3000, 5000, 10000, 15000}

def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split(',')
            command = parts[0]

            if command == "TEST":
                phone = parts[1]
                if phone.isdigit() and len(phone) == 9:
                    txn_id = str(uuid.uuid4())
                    transactions.insert_one({
                        "_id": txn_id,
                        "phone": phone,
                        "status": "PENDING",
                        "amount": None
                    })
                    client_socket.send(f"OK,{txn_id}\n".encode())
                else:
                    client_socket.send("ERROR\n".encode())

            elif command == "TOPUP":
                txn_id, phone, amount = parts[1], parts[2], int(parts[3])
                if amount in ALLOWED_AMOUNTS:
                    result = transactions.update_one(
                        {"_id": txn_id, "phone": phone},
                        {"$set": {"amount": amount, "status": "COMPLETED"}}
                    )
                    if result.matched_count:
                        client_socket.send("SUCCESS\n".encode())
                    else:
                        client_socket.send("ERROR\n".encode())
                else:
                    client_socket.send("ERROR\n".encode())

            elif command == "HISTORY":
                phone = parts[1]
                history = transactions.find({"phone": phone})
                for entry in history:
                    client_socket.send(f"{entry['_id']},{entry.get('amount', 0)},{entry['status']}\n".encode())
                client_socket.send("END\n".encode())

    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] Szerver elindult a {PORT} porton...")

    while True:
        client_sock, addr = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()

if __name__ == "__main__":
    start_server()