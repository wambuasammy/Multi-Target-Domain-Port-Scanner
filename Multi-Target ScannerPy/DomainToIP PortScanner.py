import socket
from IPy import IP

open_ports = []
# Function check_ip converts domain name into an ip address
def check_ip(ip):
    try:
        IP(ip)
        return (ip)

    except ValueError:
        return socket.gethostbyname(ip)

#Fuction scan , scans the converted ip address
def scan(target):
    converted_ip = check_ip(target)
    print("\n" + "Scanning {}".format(target))
    for port in range(1,500):
        port_scanner(converted_ip,port)



def get_banner(s):
    return s.recv(1024)

def port_scanner(ipaddress,port):
    try:
#Socket connection
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.settimeout(0.50)
        sock.connect((ipaddress,port))
        open_ports.append(port)

        try:
            banner = get_banner(sock)
            print("open port "+str(port) + ":" + str(banner.decode().strip('\n')))

        except:
            print("port " + str(port) + " open")

    except:
        return False

targets = input("Enter target/s split them with ,: ")
if ',' in targets:
    for ip_add in targets.split(','):
        scan(ip_add.strip(' '))

else:
    scan(targets)
print("Open ports are {}".format(open_ports))