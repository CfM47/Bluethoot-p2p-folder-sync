import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class FolderSync:
    def __init__(self, folder_path, server, peer_addr):
        self.folder_path = folder_path
        self.server = server
        self.peer_addr = peer_addr

    def start_sync(self):
        try:
            self.sync_existing_files()
            event_handler = FolderEventHandler(self.server, self.peer_addr)
            observer = Observer()
            observer.schedule(event_handler, self.folder_path, recursive=True)
            observer.start()
            print("Sincronización de carpeta iniciada.")

            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Sincronización detenida manualmente.")
            observer.stop()
        except Exception as e:
            print(f"Error en la sincronización: {e}")
        finally:
            observer.join()

    def sync_existing_files(self):
        try:
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    print(f"Sincronizando archivo existente: {file_path}")
                    self.server.send_file(file_path, self.peer_addr)
        except Exception as e:
            print(f"Error al sincronizar archivos existentes: {e}")


class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, server, peer_addr):
        self.server = server
        self.peer_addr = peer_addr

    def on_created(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.delete_file(event.src_path)

    def sync_file(self, file_path):
        try:
            self.server.send_file(file_path, self.peer_addr)
        except Exception as e:
            print(f"Error al sincronizar archivo {file_path}: {e}")

    def delete_file(self, file_path):
        try:
            file_name = os.path.basename(file_path)
            with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as sock:
                sock.connect((self.peer_addr, self.server.port))
                sock.sendall(f"DELETE::{file_name}".encode())
            print(f"Archivo eliminado sincronizado: {file_name}")
        except Exception as e:
            print(f"Error al sincronizar la eliminación de {file_path}: {e}")
