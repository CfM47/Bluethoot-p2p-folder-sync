import server

def main():
  local_addr = input("Enter the local Bluetooth address: ")
  folder_path = input("Enter the folder path to sync: ")
  bt_server = server.BluetoothServer(local_addr, folder_path)
  bt_server.start_server()

if __name__ == "__main__":
  main()