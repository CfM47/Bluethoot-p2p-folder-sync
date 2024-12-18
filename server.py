import socket
import os
import threading


class BluetoothServer:
    def __init__(self, local_addr, folder_path, port=30):
        self.local_addr = local_addr
        self.folder_path = folder_path
        self.port = port
        self.lock = threading.Lock()
        self.processing = threading.Event()  # Indica si el servidor está ocupado

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
            header = client_sock.recv(1024).decode()
            if header.startswith("DELETE::"):
                file_name = header.split("::", 1)[1]
                self.handle_delete(file_name)
            else:
                file_name, file_size = header.split("::")
                file_size = int(file_size)
                self.processing.set()  # Indica que el servidor está ocupado
                self.handle_received_file(client_sock, file_name, file_size)
        except Exception as e:
            print(f"Error manejando datos del cliente: {e}")
        finally:
            self.processing.clear()  # Marca el servidor como disponible
            client_sock.close()

    def handle_delete(self, file_name):
        file_path = os.path.join(self.folder_path, file_name)
        with self.lock:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Archivo eliminado: {file_name}")

    def handle_received_file(self, client_sock, file_name, file_size):
        file_path = os.path.join(self.folder_path, file_name)
        with self.lock:
            with open(file_path, 'wb') as f:
                remaining = file_size
                while remaining > 0:
                    chunk = client_sock.recv(min(1024, remaining))
                    if not chunk:
                        break
                    f.write(chunk)
                    remaining -= len(chunk)
        print(f"Archivo recibido: {file_name}")

    def send_file(self, file_path, peer_addr):
        retries = 5  # Número máximo de reintentos
        delay = 2  # Tiempo inicial de espera en segundos

        for attempt in range(1, retries + 1):
            try:
                file_name = os.path.basename(file_path)
                file_size = os.path.getsize(file_path)

                with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as sock:
                    sock.connect((peer_addr, self.port))
                    sock.sendall(f"{file_name}::{file_size}".encode())

                    with open(file_path, 'rb') as f:
                        while chunk := f.read(1024):
                            sock.sendall(chunk)

                print(f"Archivo enviado: {file_name}")
                return
            except ConnectionError as e:
                print(f"Intento {attempt} fallido al enviar archivo: {e}. Reintentando en {delay} segundos...")
                time.sleep(delay)
                delay *= 2  # Incrementa el tiempo de espera progresivamente
            except Exception as e:
                print(f"Error desconocido al enviar archivo: {e}")
                return

        print(f"No se pudo enviar el archivo {file_path} después de {retries} reintentos.")
