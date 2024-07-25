import subprocess
import platform
import time
from datetime import datetime
import threading
import tkinter as tk
from tkinter import messagebox


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
    global running, log_entries
    while running:
        if not ping(ip_address):
            log_entry = f"Connection to {ip_address} failed at {datetime.now()}\n"
            log_entries.append(log_entry)
            print(log_entry)
        else:
            print(f"Connection to {ip_address} is active.")
        time.sleep(interval)

    # Salva o log em um arquivo quando o monitoramento parar
    with open("log.txt", "w") as log_file:
        log_file.writelines(log_entries)
    print("Log saved to log.txt")


# Função para iniciar o monitoramento em uma thread separada
def start_monitoring():
    global running, monitor_thread
    ip_address = ip_entry.get()
    interval = int(interval_entry.get())

    if not ip_address or interval <= 0:
        messagebox.showerror("Input Error", "Please enter a valid IP address and interval.")
        return

    if running:
        messagebox.showinfo("Monitoring", "Monitoring is already running.")
        return

    running = True
    monitor_thread = threading.Thread(target=monitor_ip, args=(ip_address, interval))
    monitor_thread.start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)


# Função para parar o monitoramento
def stop_monitoring():
    global running
    if not running:
        messagebox.showinfo("Monitoring", "Monitoring is not running.")
        return

    running = False
    monitor_thread.join()
    messagebox.showinfo("Monitoring", "Monitoring stopped and log saved to log.txt")
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


# Configuração da interface gráfica
root = tk.Tk()
root.title("IP Monitor")

tk.Label(root, text="IP Address:").grid(row=0, column=0, padx=10, pady=10)
ip_entry = tk.Entry(root, width=30)
ip_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Interval (seconds):").grid(row=1, column=0, padx=10, pady=10)
interval_entry = tk.Entry(root, width=30)
interval_entry.grid(row=1, column=1, padx=10, pady=10)

start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring)
start_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

stop_button = tk.Button(root, text="Stop Monitoring", command=stop_monitoring, state=tk.DISABLED)
stop_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Variáveis globais
running = False
monitor_thread = None
log_entries = []

# Executa a interface gráfica
root.mainloop()