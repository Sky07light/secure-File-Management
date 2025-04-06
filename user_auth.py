import os
import json
import hashlib
import time

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password, fullname, email):
    """Register a new user"""
    users_dir = "users"
    if not os.path.exists(users_dir):
        os.makedirs(users_dir)
    
    user_file = os.path.join(users_dir, f"{username}.json")
    
    # Check if user already exists
    if os.path.exists(user_file):
        return False
    
    # Create user directory for files
    user_files_dir = os.path.join("files", username)
    if not os.path.exists(user_files_dir):
        os.makedirs(user_files_dir)
    
    # Hash password before storing
    hashed_password = hash_password(password)
