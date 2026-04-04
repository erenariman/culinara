import socket
import sys

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result == 0:
        print(f"Port {port} is OPEN (in use)")
        sys.exit(0)
    else:
        print(f"Port {port} is CLOSED (free)")
        sys.exit(1)

if __name__ == "__main__":
    check_port(3000)
