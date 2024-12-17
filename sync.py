import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading


class FolderSync:
    def __init__(self, folder_path, server):
        self.folder_path = folder_path
        self.server = server

    def start_sync(self):
        # Configura un observador para la carpeta
        event_handler = FolderEventHandler(self.server)
        observer = Observer()
        observer.schedule(event_handler, self.folder_path, recursive=True)
        observer.start()
        print("Sincronización de carpeta iniciada.")

        try:
            while True:
                time.sleep(1)  # Mantener el programa activo
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class FolderEventHandler(FileSystemEventHandler):
    def __init__(self, server):
        self.server = server
        self.synced_files = set()  # Para evitar duplicados

    def on_created(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path)

    def sync_file(self, file_path):
        if file_path not in self.synced_files:
            self.synced_files.add(file_path)
            peer_addr = input("Enter the Bluetooth address of the peer: ")
            self.server.send_file(file_path, peer_addr)
