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
