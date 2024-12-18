import socket
import os
import threading
import json

class BluetoothServer:
    def __init__(self, local_addr, folder_path, port=30):
        self.local_addr = local_addr
        self.folder_path = folder_path
        self.port = port
        self.lock = threading.Lock()

    def start_server(self):
        sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        sock.bind((self.local_addr, self.port))
        sock.listen(1)
        print(f"Servidor escuchando en {self.local_addr}:{self.port}")

        while True:
            try:
                client_sock, address = sock.accept()
                print(f"Conexión aceptada de {address}")
                threading.Thread(target=self.handle_client, args=(client_sock,)).start()
            except Exception as e:
                print(f"Error en el servidor: {e}")

    def handle_client(self, client_sock):
        try:
            data = client_sock.recv(4096)
            if data:
                self.handle_received_data(data)
        finally:
            client_sock.close()

    def handle_received_data(self, data):
        """Procesa datos recibidos como JSON y aplica cambios en la carpeta."""
        changes = json.loads(data.decode())
        with self.lock:
            for change in changes:
                action = change["action"]
                file_name = change["file_name"]
                file_path = os.path.join(self.folder_path, file_name)

                if action == "added" or action == "modified":
                    # Escribir o actualizar el archivo
                    with open(file_path, 'wb') as f:
                        f.write(change["file_data"].encode())
                    print(f"Archivo {'creado' if action == 'added' else 'modificado'}: {file_name}")
                elif action == "deleted":
                    # Eliminar el archivo local si existe
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Archivo eliminado: {file_name}")

    def send_changes(self, changes, peer_addr):
        """Envía cambios detectados al otro dispositivo."""
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as sock:
            try:
                sock.connect((peer_addr, self.port))
                sock.sendall(json.dumps(changes).encode())
                print(f"Cambios enviados: {changes}")
            except Exception as e:
                print(f"Error al enviar cambios: {e}")