# encryptor.py

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
import secrets

def derive_key(password: str, salt: bytes) -> bytes:
    """Derive a key from the password using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt_file(file_path: str, password: str):
    """Encrypt the file and delete the original."""
    salt = secrets.token_bytes(16)  # Generate a random salt
    key = derive_key(password, salt)
    fernet = Fernet(key)

    with open(file_path, 'rb') as file:
        encrypted_data = fernet.encrypt(file.read())

    with open(file_path + '.enc', 'wb') as encrypted_file:
        encrypted_file.write(salt + encrypted_data)  # Store salt with encrypted data

    os.remove(file_path)  # Delete the original file
    print(f"File '{file_path}' encrypted successfully.")