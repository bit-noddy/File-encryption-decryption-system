# decryptor.py

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

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

def decrypt_file(encrypted_file_path: str, password: str):
    """Decrypt the file and delete the encrypted version."""
    with open(encrypted_file_path, 'rb') as encrypted_file:
        salt = encrypted_file.read(16)  # Read the salt
        encrypted_data = encrypted_file.read()

    #print(f"Salt: {salt.hex()}")  # Print salt in hex format for debugging
    #print(f"Encrypted Data Length: {len(encrypted_data)}")  # Print length of encrypted data

    key = derive_key(password, salt)
    fernet = Fernet(key)

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception as e:
        print(f"Decryption failed: {e}")
        return

    with open(encrypted_file_path[:-4], 'wb') as decrypted_file:  # Remove '.enc'
        decrypted_file.write(decrypted_data)

    os.remove(encrypted_file_path)  # Delete the encrypted file
    print(f"File '{encrypted_file_path}' decrypted successfully.")