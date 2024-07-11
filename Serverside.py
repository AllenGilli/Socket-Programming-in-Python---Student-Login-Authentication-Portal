import csv
import sys
import socket
import traceback
from threading import Thread
import tkinter as tk
from tkinter import scrolledtext

# Filename of CSV file
filename = 'login_credentialss.csv'
data = {}

# Function to get IP of wifi
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("192.168.12.228", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

# Function to validate authentication
def validate_login(username, password):
    if data.get(username) is None:
        return 0
    elif data[username] == password:
        return 1
    else:
        return 0

# Read CSV file
def file_read():
    with open(filename, 'r') as login_file:
        reader = csv.reader(login_file)
        for row in reader:
            if row[0] != 'Username':
                data[row[0]] = row[1]

# Function to start the server
def start_server():
    file_read()
    host = get_ip_address()

    def connect_to_port():
        port = port_entry.get()
        port_entry.destroy()
        connect_button.destroy()
        text_box.insert(tk.END, "Hostname: " + host + "\n")
        text_box.insert(tk.END, "Port: " + port + "\n")
        text_box.insert(tk.END, 'Socket is now listening!\n')
        text_box.insert(tk.END, '*' * 40 + "\n")
        window.update()  # Update the GUI window

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            server_socket.bind((host, int(port)))
        except:
            text_box.insert(tk.END, "Bind Failed! Error: " + str(sys.exc_info()) + "\n")
            return

        server_socket.listen(5)

        def handle_clients():
            while True:
                # Connect to a client
                client_socket, address = server_socket.accept()
                ip, port = str(address[0]), str(address[1])
                text_box.insert(tk.END, "Connected with " + ip + " : " + port + "\n")
                window.update()  # Update the GUI window

                try:
                    Thread(target=client, args=(client_socket, ip, port)).start()
                except:
                    text_box.insert(tk.END, "Thread did not start.\n")
                    traceback.print_exc()
                    window.update()  # Update the GUI window

        client_thread = Thread(target=handle_clients)
        client_thread.start()

    window = tk.Tk()
    window.title("Server Log")

    port_label = tk.Label(window, text="Enter Port:")
    port_label.pack()

    port_entry = tk.Entry(window)
    port_entry.pack()
    port_entry.focus_set()

    connect_button = tk.Button(window, text="Start Server", command=connect_to_port)
    connect_button.pack()

    text_box = scrolledtext.ScrolledText(window)
    text_box.pack()

    window.mainloop()

# Function to interact with client
def client(client_socket, ip, port):
    # Get username and password
    username = client_socket.recv(1024).decode()
    client_socket.send(('ACK : Username received!').encode())
    print("Username received from " + ip + ":" + port)

    password = client_socket.recv(1024).decode()
    client_socket.send(('ACK : Password received!').encode())
    print("Password received from " + ip + ":" + port)

    # Validate authentication
    if validate_login(username, password) == 1:
        client_socket.send(('1').encode())
    else:
        client_socket.send(('0').encode())

    # Close client socket
    client_socket.close()
    print("Connection " + ip + ":" + port + " closed!")
    print('*' * 40)

# Main function
def main():
    file_read()
    start_server()

# Run the main function
if __name__ == '__main__':
    main()
