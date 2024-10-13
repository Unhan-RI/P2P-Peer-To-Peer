import socket
import threading
import time
import random
import os


received_messages = set()


neighbors = []


def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Node berjalan sebagai server di {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()


def handle_client(conn, addr):
    global received_messages
    while True:
        try:
            
            header = conn.recv(1024).decode()
            if header.startswith("MESSAGE"):
                message = header[len("MESSAGE "):]
                
                if message not in received_messages:
                    print(f"Pesan diterima: {message} dari {addr}")
                    received_messages.add(message)
                    flood_message(message)
            elif header.startswith("FILE"):
                file_name, file_size = header.split()[1:3]
                file_size = int(file_size)

                
                receive_file(conn, file_name, file_size)
                
        except Exception as e:
            print(f"Error menerima pesan dari {addr}: {e}")
            break
    conn.close()


def receive_file(conn, file_name, file_size):
    with open(file_name, 'wb') as f:
        bytes_received = 0
        while bytes_received < file_size:
            data = conn.recv(1024)
            f.write(data)
            bytes_received += len(data)
        print(f"File {file_name} berhasil diterima dan disimpan.")
    flood_file(file_name, file_size)


def flood_message(message):
    global neighbors
    for neighbor in neighbors:
        try:
            neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            neighbor_socket.connect(neighbor)
            neighbor_socket.send(f"MESSAGE {message}".encode())
            neighbor_socket.close()
        except Exception as e:
            print(f"Error mengirim pesan ke {neighbor}: {e}")


def flood_file(file_name, file_size):
    global neighbors
    for neighbor in neighbors:
        try:
            neighbor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            neighbor_socket.connect(neighbor)
            neighbor_socket.send(f"FILE {file_name} {file_size}".encode())
            send_file(neighbor_socket, file_name)
            neighbor_socket.close()
        except Exception as e:
            print(f"Error mengirim file ke {neighbor}: {e}")


def send_file(sock, file_name):
    with open(file_name, 'rb') as f:
        data = f.read(1024)
        while data:
            sock.send(data)
            data = f.read(1024)
    print(f"File {file_name} berhasil dikirim.")


def start_node(host, port, neighbor_list):
    global neighbors
    neighbors = neighbor_list
    threading.Thread(target=start_server, args=(host, port)).start()

    time.sleep(2)  

    while True:
        choice = input("Pilih (1) untuk kirim pesan, (2) untuk kirim file, (ketik 'exit' untuk keluar): ")
        if choice == '1':
            message = input("Masukkan pesan untuk flooding: ")
            flood_message(f"{host}:{port} -> {message}")
        elif choice == '2':
            file_name = input("Masukkan nama file untuk dikirim: ")
            if os.path.exists(file_name):
                file_size = os.path.getsize(file_name)
                flood_file(file_name, file_size)
            else:
                print(f"File {file_name} tidak ditemukan.")
        elif choice.lower() == 'exit':
            break

if __name__ == "__main__":
    
    host = '10.2.55.46'
    port = 15006

    
    neighbors = [('10.2.55.83', 5009), ('127.0.0.1', 5002)]  


    start_node(host, port, neighbors)

