import socket
import time
import random
import threading
import uuid
import re
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://matyika123456:H4FdxLQcNMOQvoBT@transactiondb.fcusdo6.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client['TransactionDB']
transactions = db['Transactions']

HOST = '0.0.0.0'
PORT = 5000
ALLOWED_AMOUNTS = {3000, 5000, 10000, 15000}

def normalize_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if digits.startswith("36") and len(digits) >= 11:
        return digits[-9:]
    elif digits.startswith("06") and len(digits) >= 11:
        return digits[-9:]
    elif len(digits) == 9:
        return digits
    else:
        return None
    
def handle_client(client_socket):
    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split(',')
            command = parts[0]

            if command == "TEST":
                phone = normalize_phone(parts[1])
                if phone:
                    txn_id = str(uuid.uuid4())
                    transactions.insert_one({
                        "_id": txn_id,
                        "phone": phone,
                        "status": "PENDING",
                        "amount": None,
                        "validated": True
                    })
                    client_socket.send(f"OK,{txn_id}\n".encode())
                else:
                    client_socket.send("ERROR\n".encode())

            elif command == "TOPUP":
                txn_id, phone, amount = parts[1], normalize_phone(parts[2]), int(parts[3])
                if phone and amount in ALLOWED_AMOUNTS:
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
                phone = normalize_phone(parts[1])
                if phone:
                    history = transactions.find({"phone": phone})
                    for entry in history:
                        client_socket.send(f"{entry['_id']},{entry.get('amount', 0)},{entry['status']}\n".encode())
                client_socket.send("END\n".encode())
    finally:
        client_socket.close()

def auto_topup_pending_transactions():
    while True:
        pending = list(transactions.find({
            "status": "PENDING",
            "amount": None,
            "validated": True
        }))
        for txn in pending:
            txn_id = txn["_id"]
            phone = txn["phone"]
            amount = random.choice(list(ALLOWED_AMOUNTS))
            result = transactions.update_one(
                {"_id": txn_id, "phone": phone, "status": "PENDING"},
                {"$set": {"amount": amount, "status": "COMPLETED"}}
            )
            if result.modified_count:
                print(f"[AUTO_TOPUP] Transaction {txn_id} for {phone} topped up with {amount} HUF.")
        time.sleep(5)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"[+] Server started on port {PORT}...")
    
    threading.Thread(target=auto_topup_pending_transactions, daemon=True).start()

    while True:
        client_sock, _ = server.accept()
        threading.Thread(target=handle_client, args=(client_sock,), daemon=True).start()