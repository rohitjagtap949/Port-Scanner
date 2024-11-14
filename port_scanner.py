import socket
import threading
from queue import Queue

NUM_THREADS = 100

queue = Queue()

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                service = socket.getservbyport(port)
                print(f"Open Port: {port}, Service: {service}")
            except:
                service = "Unknown"
                print(f"Open Port: {port}, Service: {service}")
        sock.close()
    except socket.error:
        pass

def worker(ip):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port)
        queue.task_done()

def scan_ip(ip, start_port, end_port):
    print(f"Scanning IP Using Redcyberfox Port Scanner: {ip}")
    for port in range(start_port, end_port + 1):
        queue.put(port)

    for _ in range(NUM_THREADS):
        thread = threading.Thread(target=worker, args=(ip,))
        thread.start()

    queue.join()

def scan_network(start_ip, end_ip, start_port, end_port):
    start_ip_list = list(map(int, start_ip.split('.')))
    end_ip_list = list(map(int, end_ip.split('.')))

    for i in range(start_ip_list[3], end_ip_list[3] + 1):
        ip = f"{start_ip_list[0]}.{start_ip_list[1]}.{start_ip_list[2]}.{i}"
        scan_ip(ip, start_port, end_port)

def main():
    start_ip = input("Welcome To Redcyberfox!!!!!! Enter the start IP address (e.g., 192.168.1.1): ")
    end_ip = input("Enter the end IP address (e.g., 192.168.1.10): ")
    start_port = int(input("Enter the start port (e.g., 20): "))
    end_port = int(input("Enter the end port (e.g., 1024): "))

    scan_network(start_ip, end_ip, start_port, end_port)

if __name__ == "__main__":
    main()