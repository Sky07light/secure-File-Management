import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ENCRYPTION_KEY = b'SecureFileX-EncryptionKey-2023'
SALT = b'SecureFileXSalt12345'

def get_encryption_key(password=None):
    """Generate an encryption key from password or use default"""
    if not password:
        password = ENCRYPTION_KEY
        
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=SALT,
        iterations=100000
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key

def encrypt_file(file_path, password=None):
    """Encrypt a file in-place"""
    try:
        # Generate key
        key = get_encryption_key(password)
        fernet = Fernet(key)
        
        # Read file
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        # Encrypt data
        encrypted_data = fernet.encrypt(file_data)
        
        # Write encrypted data back to file
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
            
        return True
    except Exception as e:
        print(f"Encryption error: {str(e)}")
        return False

def decrypt_file(file_path, password=None):
    """Decrypt a file in-place"""
    try:
        # Generate key
        key = get_encryption_key(password)
        fernet = Fernet(key)
        
        # Read encrypted file
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        # Decrypt data
        decrypted_data = fernet.decrypt(encrypted_data)
        
        # Write decrypted data back to file
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
            
        return True
    except Exception as e:
        print(f"Decryption error: {str(e)}")
        return False
        
