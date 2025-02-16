<h1 align="center">Documentation</h1>
<div align="center">
    <a href="/README.md">English</a>
    <a href="/README_ru.md">Русский</a>
    <br><br>
</div>

This Python FTP-like solution enables secure file transfers between devices on local networks. The multi-threaded server handles concurrent connections while the cross-platform client offers both CLI and interactive modes. Features include command-line arguments, session persistence, and basic error handling.

# server.py
A multi-threaded FTP-like file server supporting:
- File upload/download for all file types
- Directory navigation (CD command)
- File listing (LIST command)
- Automatic local IP detection
- Cross-platform console clearing
- Client connection management

Key Features:
- Uses TCP sockets on port 5001
- Maintains separate client sessions
- Stores files in "server_files" directory
- Handles multiple concurrent connections
- Basic error handling

# client.py
A feature-rich client with:
- Interactive and CLI modes
- Command-line arguments support:
  - `-i IP` - Server IP
  - `-p PORT` - Server port
  - `-l` - List server files
  - `-u FILE` - Upload file
  - `-d FILE` - Download file
  - `-h` - Show help
- Local IP detection
- Session history preservation
- Cross-platform compatibility
- Auto-completion for common commands
