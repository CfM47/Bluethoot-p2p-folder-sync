import socket
import os

class BluetoothServer:
  def __init__(self, local_addr, folder_path, port=30):
    self.local_addr = local_addr
    self.folder_path = folder_path
    self.port = port

  def start_server(self):
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.bind((self.local_addr, self.port))
    sock.listen(1)
    print(f"Servidor escuchando en {self.local_addr}:{self.port}")

    while True:
      client_sock, address = sock.accept()
      print(f"Conexión aceptada de {address}")
      data = client_sock.recv(1024)
      if data:
        self.handle_received_data(data)
      client_sock.close()

  def handle_received_data(self, data):
    file_name, file_data = data.decode().split('::', 1)
    file_path = os.path.join(self.folder_path, file_name)
    with open(file_path, 'wb') as f:
      f.write(file_data.encode())
    print(f"Archivo recibido: {file_name}")

  def send_file(self, file_path, peer_addr):
    with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as sock:
      sock.connect((peer_addr, self.port))
      file_name = os.path.basename(file_path)
      with open(file_path, 'rb') as f:
        file_data = f.read()
      sock.sendall(f"{file_name}::{file_data.decode()}".encode())
    print(f"Archivo enviado: {file_name}")