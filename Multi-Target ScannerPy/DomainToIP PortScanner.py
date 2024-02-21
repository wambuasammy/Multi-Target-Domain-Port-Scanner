import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from IPy import IP

lock = threading.Lock()  # Lock to synchronize access to shared resources

def check_ip(ip):
    """
    Check if the input is a valid IP address or hostname and return the corresponding IP address.
    """
    try:
        IP(ip)
        return ip
    except ValueError:
        return socket.gethostbyname(ip)

def scan(target, start_port, end_port, open_ports_dict):
    """
    Scan the specified range of ports for the given target.
    """
    converted_ip = check_ip(target)
    open_ports_dict[target] = {}  # Initialize dictionary for the current target
    print("\n" + f"Scanning {target} for ports {start_port}-{end_port}")

    with ThreadPoolExecutor(max_workers=30) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(port_scanner, converted_ip, port, open_ports_dict[target])

def port_scanner(ipaddress, port, open_ports_dict):
    """
    Attempt to connect to the specified port on the target IP address.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.50)  # Set a timeout for the connection attempt
        result = sock.connect_ex((ipaddress, port))
        if result == 0:
            with lock:
                open_ports_dict[port] = 'open'  # Store open port for the current target
                print("Open port {} on {}".format(port, ipaddress))
        sock.close()

    except Exception as e:
        pass

# Get user input for targets, start port, and end port
targets = input("Enter target/s split them with ,: ")
start_port = int(input("Enter the start port number: "))
end_port = int(input("Enter the end port number: "))

open_ports_dict = {}  # Initialize dictionary to store open ports for each target

# Scan each target for open ports using multithreading
if ',' in targets:
    for ip_add in targets.split(','):
        scan(ip_add.strip(), start_port, end_port, open_ports_dict)
else:
    scan(targets, start_port, end_port, open_ports_dict)

# Print open ports for each target after scanning all targets
print("\nOpen ports for each target:")
for target, ports_dict in open_ports_dict.items():
    print(f"{target}: {ports_dict}")
