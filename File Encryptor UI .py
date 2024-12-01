import tkinter as tk
from tkinter import filedialog, messagebox
import os  # Import the os module
from encryptor import encrypt_file
from decryptor import decrypt_file

# Function to select a file path
def select_file(entry):
    file_path = filedialog.askopenfilename()
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

# Function to encrypt a file
def encrypt_action():
    file_path = file_path_entry.get().strip()
    password = password_entry.get().strip()

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "File not found. Please select a valid file.")
        return
    if len(password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters long.")
        return

    try:
        encrypt_file(file_path, password)
        messagebox.showinfo("Success", "File encrypted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {e}")

# Function to decrypt a file
def decrypt_action():
    file_path = file_path_entry.get().strip()
    password = password_entry.get().strip()

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "File not found. Please select a valid file.")
        return
    if len(password) < 8:
        messagebox.showerror("Error", "Password must be at least 8 characters long.")
        return

    try:
        decrypt_file(file_path, password)
        messagebox.showinfo("Success", "File decrypted successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {e}")

# Create the main application window
app = tk.Tk()
app.title("File Encryptor/Decryptor")
app.geometry("400x250")

# File path selection
tk.Label(app, text="File Path:").pack(pady=5)
file_path_entry = tk.Entry(app, width=40)
file_path_entry.pack(pady=5)
tk.Button(app, text="Browse", command=lambda: select_file(file_path_entry)).pack(pady=5)

# Password input
tk.Label(app, text="Password:").pack(pady=5)
password_entry = tk.Entry(app, show="*", width=40)
password_entry.pack(pady=5)

# Buttons for encryption and decryption (aligned horizontally)
button_frame = tk.Frame(app)  # Create a frame to hold the buttons
button_frame.pack(pady=10)

encrypt_button = tk.Button(button_frame, text="Encrypt", command=encrypt_action, width=15)
encrypt_button.pack(side=tk.LEFT, padx=5)

decrypt_button = tk.Button(button_frame, text="Decrypt", command=decrypt_action, width=15)
decrypt_button.pack(side=tk.LEFT, padx=5)

# Run the application
app.mainloop()
