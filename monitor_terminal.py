import subprocess
import platform
import time
from datetime import datetime

# Função para enviar ping
def ping(ip_address, count=1, timeout=2):
    try:
        if platform.system().lower() == "windows":
            command = ["ping", "-n", str(count), "-w", str(timeout * 1000), ip_address]
        else:
            command = ["ping", "-c", str(count), "-W", str(timeout), ip_address]

        output = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        success_indicator = "TTL=" if platform.system().lower() == "windows" else "time="
        return success_indicator in output.stdout
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Função de monitoramento
def monitor_ip(ip_address, interval=5):
    log_entries = []
    while True:
        if not ping(ip_address):
            log_entry = f"Connection to {ip_address} failed at {datetime.now()}\n"
            log_entries.append(log_entry)
            print(log_entry)
        else:
            print(f"Connection to {ip_address} is active.")
        time.sleep(interval)

if __name__ == "__main__":
    import sys
    ip_address = sys.argv[1]
    interval = int(sys.argv[2])
    monitor_ip(ip_address, interval)
