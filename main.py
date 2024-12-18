import server
import sync
import threading


def main():
    local_addr = input("Ingrese la dirección Bluetooth local: ")
    folder_path = input("Ingrese la ruta de la carpeta a sincronizar: ")
    peer_addr = input("Ingrese la dirección Bluetooth del par: ")

    # Crear una instancia del servidor Bluetooth
    bt_server = server.BluetoothServer(local_addr, folder_path)

    # Iniciar el servidor en un hilo separado
    server_thread = threading.Thread(target=bt_server.start_server, daemon=True)
    server_thread.start()
    print("Servidor Bluetooth iniciado.")

    # Crear una instancia de FolderSync y pasar la dirección del par
    sync_monitor = sync.FolderSync(folder_path, bt_server, peer_addr)
    sync_monitor.start_sync()  # Iniciar la monitorización de la carpeta


if __name__ == "__main__":
    main()
