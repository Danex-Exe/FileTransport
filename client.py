import socket, os, platform, sys

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
print('Ваш локальный IP адрес: '+ get_local_ip() + "\n")

server_host = get_local_ip()
server_port = 5001
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


clear()
def upload_file(filename):
    try:
        filesize = os.path.getsize(filename)
        client_socket.send(f"UPLOAD".encode())
        client_socket.send(f"{filename}{SEPARATOR}{filesize}".encode())
        
        with open(filename, "rb") as f:
            while True:
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read: break
                client_socket.sendall(bytes_read)
        response = client_socket.recv(BUFFER_SIZE).decode()
        print(response)
    except Exception as e: print(f"Ошибка загрузки: {e}")

def download_file(filename):
    client_socket.send(f"DOWNLOAD {filename}".encode())
    response = client_socket.recv(BUFFER_SIZE).decode()
    
    if response == "Файл не найден":
        print(response)
        return

    filename, filesize = response.split(SEPARATOR)
    filesize = int(filesize)
    
    with open(filename, "wb") as f:
        bytes_received = 0
        while bytes_received < filesize:
            bytes_read = client_socket.recv(BUFFER_SIZE)
            if not bytes_read: break
            f.write(bytes_read)
            bytes_received += len(bytes_read)
    print(f"Файл {filename} успешно скачан")

def list_files():
    client_socket.send("LIST".encode())
    file_list = client_socket.recv(BUFFER_SIZE).decode()
    print("\nСодержимое сервера:")
    print(file_list)

def change_directory(dirname):
    client_socket.send(f"CD {dirname}".encode())
    response = client_socket.recv(BUFFER_SIZE).decode()
    print(response)

def show_help():
    print("""\nДоступные команды:
\tupload <filename> - Загрузить файл на сервер
\tdownload <filename> - Скачать файл с сервера
\tlist - Показать файлы на сервере
\tcd <directory> - Сменить директорию на сервере
\tclear - Очистить консоль
\thelp - Показать справку
\texit - Выйти\n""")

def main() -> None:
    global server_host, server_port
    if len(sys.argv) > 1:
        args = sys.argv[1:]
        if len(args) > 1 or args[0] in ['-l', '-h']:
            argv = {}
            current = ''
            for i in args:
                if i.startswith('-'):
                    current = (i[1:] if i.startswith('--') else i[1:]).lower()
                    if current in argv:
                        print('Аргумент {} уже был указан'.format(current))
                        quit()
                    argv[current] = ""
                else:
                    if "" == argv[current] and current not in ['h', 'l']: argv[current] = i
                    else:
                        print("""Используйте
\t-i IP - IP адрес сервера
\t-p PORT - Порт сервера
\t-l - Показать файлы на сервере
\t-u FILE - Загрузить файл на сервер
\t-d FILE - Скачать файл с сервера
\t-h - Показать справку""")
                        quit()
            for i in argv:
                if i not in ['h', 'l']:
                    if argv[i] == '': 
                        print('Значение аргумента {} не было указано'.format(i))
                        quit()
            for i in argv:
                match i:
                    case 'i': server_host = argv[i]
                    case 'p':
                        try: server_port = int(argv[i])
                        except: 
                            print("Вы ввели неверный порт!") 
                            quit()
                    case 'l': connect('list')
                    case 'u': connect('upload', argv[i])
                    case 'd': connect('download', argv[i])
                    case 'h': show_help()
        else:
            print("""Используйте
\t-ip IP - IP адрес сервера
\t-port PORT - Порт сервера
\t-list - Показать файлы на сервере
\t-u FILE - Загрузить файл на сервер
\t-d FILE - Скачать файл с сервера
\t-h - Показать справку""")
            quit()
    else:
        server_host = input("Введите IP сервера, или нажмите Enter чтобы использовать локальный IP: ")
        server_host = server_host if len(server_host) >= 6 else get_local_ip()
        server_port = input("Введите IP сервера, или нажмите Enter чтобы использовать обычный (5001): ")
        try: server_port = int(server_port) if len(server_port) >= 4 else 5001
        except:
            print("Вы ввели неверный порт!")
            quit()
        clear()
        connect()

def check_command(command: str, client_socket, arg: str = None):
    match command:
        case "exit":
            client_socket.send("EXIT".encode())
            return True
        case "clear": clear()
        case "cls": clear()
        case "list": list_files()
        case "cd": change_directory(arg)
        case "upload":
            if os.path.exists(arg): upload_file(arg)
            else: print("Файл не существует")
        case "download": download_file(arg)
        case "help": show_help()
        case _: print("Неизвестная команда")


def connect(command: str = None, arg: str = None) -> None:
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((server_host, server_port))
        if command is None:
            print(f"Подключено к {server_host}:{server_port}")
            show_help()
            while True:
                command = input("Введите команду: ").strip()
                if check_command(command.lower().split()[0], client_socket, command.split()[1]): break 
        else: 
            check_command(command, client_socket, arg)
            print()

    except Exception as e: print(f"Ошибка: {e}")
    finally: client_socket.close()

if __name__ == "__main__":
    main()