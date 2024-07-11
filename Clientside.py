import socket
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog

# Create the GUI window
window = tk.Tk()
window.title("Client")

# Create a text box to display messages
text_box = tk.Text(window, height=10, width=40)
text_box.pack()

def connect_to_server():
    ip = simpledialog.askstring("Server IP", "Enter hostname of server:")
    port = simpledialog.askstring("Server Port", "Enter Port:")
    welcome_msg = ('-' * 20) + 'WELCOME!' + ('-' * 20)
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect((ip, int(port)))
        text_box.insert(tk.END, 'Connection Successful!\n')
        text_box.insert(tk.END, welcome_msg + '\n')
    except:
        text_box.insert(tk.END, "Connection Error!\n")
        return
    
    username = simpledialog.askstring("Username", "Enter Username:")
    client_socket.send(username.encode())
    text_box.insert(tk.END, client_socket.recv(1024).decode() + '\n')
    
    password = simpledialog.askstring("Password", "Enter Password:", show="*")
    client_socket.send(password.encode())
    text_box.insert(tk.END, client_socket.recv(1024).decode() + '\n')
    
    validate_bit = client_socket.recv(1024).decode()
    
    if validate_bit == '0':
        text_box.insert(tk.END, 'Invalid Username/Password!\n')
        client_socket.close()
    else:
        text_box.insert(tk.END, 'Authentication Successful!\n')
        text_box.insert(tk.END, 'Socket closed!\n')

# Create a button to connect to the server
connect_button = tk.Button(window, text="Connect to Server", command=connect_to_server)
connect_button.pack()

# Start the GUI main loop
window.mainloop()
