import socket
import random
import time
import threading

def run_client(name, phone_list):
    while True:
        phone = random.choice(phone_list)
        sock = socket.socket()
        sock.connect(('localhost', 5000))

        # Step 1: TEST
        sock.send(f"TEST,{phone}\n".encode())
        response = sock.recv(1024).decode().strip()
        if response.startswith("OK"):
            txn_id = response.split(',')[1]
            # Step 3: TOPUP
            amount = random.choice([3000, 5000, 10000, 15000])
            sock.send(f"TOPUP,{txn_id},{phone},{amount}\n".encode())
            result = sock.recv(1024).decode().strip()
            print(f"[{name}] TOPUP result: {result}")
        else:
            print(f"[{name}] TEST failed for {phone}")
        sock.close()
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    phone_numbers = ["123456789", "987654321", "112233445"]
    for i in range(3):
        threading.Thread(target=run_client, args=(f"ATM-{i+1}", phone_numbers), daemon=True).start()

    while True:
        time.sleep(1)