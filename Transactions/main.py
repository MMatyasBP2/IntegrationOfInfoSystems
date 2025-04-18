import threading
import time
from server_module import start_server
from client_module import run_client

if __name__ == "__main__":
    phone_numbers = ["+36/70-249-7372", "+36/70-258-0094", "+36/20-620-6280"]
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)

    for i in range(3):
        threading.Thread(
            target=run_client,
            args=(f"ATM-{i+1}", phone_numbers),
            daemon=True
        ).start()

    while True:
        time.sleep(1)