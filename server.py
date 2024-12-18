import socket
import os
import threading


class BluetoothServer:
    def __init__(self, local_addr, folder_path, port=30):
        self.local_addr = local_addr
        self.folder_path = folder_path
        self.port = port
        self.lock = threading.Lock()

    def start_server(self):
        try:
            sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            sock.bind((self.local_addr, self.port))
            sock.listen(1)
            print(f"Servidor escuchando en {self.local_addr}:{self.port}")
        except Exception as e:
            print(f"Error al iniciar el servidor Bluetooth: {e}")
            return

        while True:
            try:
                client_sock, address = sock.accept()
                print(f"Conexión aceptada de {address}")
                threading.Thread(target=self.handle_client, args=(client_sock,)).start()
            except Exception as e:
                print(f"Error aceptando conexión: {e}")

    def handle_client(self, client_sock):
        try:
            data = client_sock.recv(1024)
            if data:
                self.handle_received_data(data)
        except Exception as e:
            print(f"Error manejando datos del cliente: {e}")
        finally:
            client_sock.close()

    def handle_received_data(self, data):
        try:
            if data.startswith(b"DELETE::"):
                file_name = data.decode().split("::", 1)[1]
                file_path = os.path.join(self.folder_path, file_name)
                with self.lock:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        print(f"Archivo eliminado: {file_name}")
            else:
                file_name, file_data = data.decode().split("::", 1)
                file_path = os.path.join(self.folder_path, file_name)

                with self.lock:
                    with open(file_path, 'wb') as f:
                        f.write(file_data.encode())
                print(f"Archivo recibido: {file_name}")
        except Exception as e:
            print(f"Error al procesar los datos recibidos: {e}")

    def send_file(self, file_path, peer_addr):
        try:
            with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as sock:
                sock.connect((peer_addr, self.port))
                file_name = os.path.basename(file_path)
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                sock.sendall(f"{file_name}::{file_data.decode()}".encode())
                print(f"Archivo enviado: {file_name}")
        except FileNotFoundError:
            print(f"Archivo no encontrado: {file_path}")
        except ConnectionError as e:
            print(f"Error de conexión al enviar archivo: {e}")
        except Exception as e:
            print(f"Error desconocido al enviar archivo: {e}")
