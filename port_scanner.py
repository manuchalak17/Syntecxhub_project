import socket
import threading
from datetime import datetime

print_lock = threading.Lock()
LOG_FILE = "scan_results.txt"


def log_result(text):
    with open(LOG_FILE, "a") as f:
        f.write(f"{datetime.now()} | {text}\n")


def scan_port(host, port, timeout=1):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)

        result = sock.connect_ex((host, port))
        sock.close()

        with print_lock:
            if result == 0:
                msg = f"Port {port} -> OPEN"
            else:
                msg = f"Port {port} -> CLOSED"

            print(msg)
            log_result(msg)

    except socket.timeout:
        with print_lock:
            msg = f"Port {port} -> TIMEOUT"
            print(msg)
            log_result(msg)

    except Exception as e:
        with print_lock:
            msg = f"Port {port} -> ERROR ({e})"
            print(msg)
            log_result(msg)


def main():
    print("=" * 50)
    print("        TCP PORT SCANNER")
    print("=" * 50)

    host = input("Enter host (IP or domain): ").strip()

    try:
        start_port = int(input("Enter start port: "))
        end_port = int(input("Enter end port: "))
    except ValueError:
        print("Ports must be numeric")
        return

    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print("Invalid host")
        return

    print(f"\nScanning host: {target_ip}")
    print(f"Ports: {start_port} to {end_port}")
    print("Scan started...\n")

    start_time = datetime.now()
    threads = []

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scan_port, args=(target_ip, port))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_time = datetime.now()

    print("\nScan completed!")
    print(f"Time taken: {end_time - start_time}")
    print(f"Results saved in: {LOG_FILE}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan interrupted by user")
