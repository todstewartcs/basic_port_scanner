import argparse
from socket import *
import threading
screenLock = threading.Semaphore()

def connectionScan(target_host, target_port):
    try:
        connection_socket = socket(AF_INET, SOCK_STREAM)
        connection_socket.settimeout()
        connection_socket.connect((target_host, target_port))
        connection_socket.send('ViolentPython\r\n')
        results = connection_socket.recv(100)
        screenLock.acquire()
        print("[+] {:d}/tcp open".format(target_port))
        print("[+] " + str(results))
    except:
        screenLock.acquire()
        print("[-] {:d}/tcp closed".format(target_port))
    finally:
        screenLock.release()
        connection_socket.close()


def portScan(target_host, target_ports):
    try:
        target_IP = gethostbyname(target_host)
    except:
        print("[-]Cannot resolve {:s}: Unknown host".format(target_host))
        return
    try:
        target_name = gethostbyaddr(target_IP)
        print("\n[+] Scan results for: " + target_name[0])
    except:
        print("\n[+] Scan results for: " + target_IP)
    setdefaulttimeout(1)
    for target_port in target_ports:
        print("Scanning port " + target_port)
        t = threading.Thread(target=connectionScan, args=(target_host, int(target_port)))
        t.start()


def main():
    parser = argparse.ArgumentParser(description="Process host name and port number", prog="HOST/PORT PARSER")
    parser.add_argument('-H', dest='target_host', type=str, help='specify target host')
    parser.add_argument('-p', dest='target_port', type=str, help='specify target port(s) separated by comma')
    args = parser.parse_args()
    target_host = args.target_host
    target_ports = str(args.target_port).split(",")
    if (target_host is None) | (target_ports[0] is None):
        print(parser.usage)
        exit()
    portScan(target_host, target_ports)

if __name__ == '__main__':
    main()
