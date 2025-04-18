import socket
import random
import time

def run_client(name, phone_list):
    while True:
        try:
            sock = socket.socket()
            sock.connect(('localhost', 5000))
            phone = random.choice(phone_list)
            action = random.choice(['TEST', 'TOPUP'])

            if action == 'TEST':
                sock.send(f"TEST,{phone}\n".encode())
                response = sock.recv(1024).decode().strip()
                print(f"[{name}] TEST result: {response}")

            elif action == 'TOPUP':
                sock.send(f"TEST,{phone}\n".encode())
                response = sock.recv(1024).decode().strip()
                if response.startswith("OK"):
                    txn_id = response.split(',')[1]
                    amount = random.choice([3000, 5000, 10000, 15000])
                    sock.send(f"TOPUP,{txn_id},{phone},{amount}\n".encode())
                    result = sock.recv(1024).decode().strip()
                    print(f"[{name}] TOPUP result: {result}")
                else:
                    print(f"[{name}] TEST before TOPUP failed for {phone}")
        except Exception as e:
            print(f"[{name}] Exception: {e}")
        finally:
            sock.close()
            time.sleep(random.uniform(1, 3))