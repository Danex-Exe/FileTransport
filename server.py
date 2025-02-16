import socket, os, threading, platform

clear = lambda: os.system('cls' if platform.system() == 'Windows' else 'clear')
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Ошибка при получении локального IP: {e}")
        return None
clear()

SERVER_HOST = get_local_ip()
SERVER_PORT = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
SERVER_FILES = "server_files"

def handle_client(client_socket):
    current_dir = SERVER_FILES
    try:
        while True:
            command = client_socket.recv(BUFFER_SIZE).decode()
            if not command: break
            if command.startswith("UPLOAD"):
                file_info = client_socket.recv(BUFFER_SIZE).decode()
                filename, filesize = file_info.split(SEPARATOR)
                filename = os.path.basename(filename)
                filesize = int(filesize)
                file_path = os.path.join(current_dir, filename)
                with open(file_path, "wb") as f:
                    bytes_received = 0
                    while bytes_received < filesize:
                        bytes_read = client_socket.recv(BUFFER_SIZE)
                        if not bytes_read: break
                        f.write(bytes_read)
                        bytes_received += len(bytes_read)
                client_socket.send("Файл успешно загружен".encode())

            elif command.startswith("DOWNLOAD"):
                filename = command.split()[1]
                file_path = os.path.join(current_dir, filename)
                if os.path.exists(file_path):
                    filesize = os.path.getsize(file_path)
                    client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
                    with open(file_path, "rb") as f:
                        while True:
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read: break
                            client_socket.sendall(bytes_read)
                else: client_socket.send("Файл не найден".encode())

            elif command == "LIST":
                files = os.listdir(current_dir)
                file_list = "\n".join(files) if files else "Каталог пуст"
                client_socket.send(file_list.encode())

            elif command.startswith("CD"):
                new_dir = command.split()[1]
                if os.path.isdir(os.path.join(current_dir, new_dir)):
                    current_dir = os.path.join(current_dir, new_dir)
                    client_socket.send(f"Перешел в директорию: {current_dir}".encode())
                else: client_socket.send("Директория не существует".encode())
            elif command == "EXIT": break

    except Exception as e: print(f"Ошибка: {e}")
    finally: client_socket.close()

def main():
    if not os.path.exists(SERVER_FILES): os.makedirs(SERVER_FILES)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((SERVER_HOST, SERVER_PORT))
    server.listen(5)
    print(f"[*] Сервер слушает на {SERVER_HOST}:{SERVER_PORT}")
    while True:
        client_socket, address = server.accept()
        print(f"[+] Подключен клиент {address[0]}:{address[1]}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__": main()