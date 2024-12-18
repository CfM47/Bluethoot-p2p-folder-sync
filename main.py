import server
import sync
import threading


def main():
    local_addr = input("Enter the local Bluetooth address: ")
    folder_path = input("Enter the folder path to sync: ")
    peer_addr = input("Enter the Bluetooth address of the peer: ")  # Agregar peer_addr

    bt_server = server.BluetoothServer(local_addr, folder_path)

    server_thread = threading.Thread(target=bt_server.start_server, daemon=True)
    server_thread.start()
    print("Servidor Bluetooth iniciado.")

    sync_monitor = sync.FolderSync(folder_path, bt_server, peer_addr)
    sync_monitor.start_sync()


if __name__ == "__main__":
    main()
