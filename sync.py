import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FolderSync:
    def __init__(self, folder_path, server, peer_addr):
        self.folder_path = folder_path
        self.server = server
        self.peer_addr = peer_addr

    def start_sync(self):
        # Configura un observador para la carpeta
        event_handler = FolderEventHandler(self.folder_path, self.server, self.peer_addr)
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
    def __init__(self, folder_path, server, peer_addr):
        self.folder_path = folder_path
        self.server = server
        self.peer_addr = peer_addr

    def on_created(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path, "added")

    def on_modified(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path, "modified")

    def on_deleted(self, event):
        if not event.is_directory:
            self.sync_file(event.src_path, "deleted")

    def sync_file(self, file_path, action):
        """Envía información del cambio al servidor."""
        file_name = os.path.relpath(file_path, self.folder_path)
        changes = []

        if action in ["added", "modified"]:
            with open(file_path, 'rb') as f:
                file_data = f.read().decode()
            changes.append({
                "action": action,
                "file_name": file_name,
                "file_data": file_data,
            })
        elif action == "deleted":
            changes.append({
                "action": action,
                "file_name": file_name,
            })

        self.server.send_changes(changes, self.peer_addr)