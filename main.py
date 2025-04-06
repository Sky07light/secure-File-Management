import tkinter as tk
from tkinter import messagebox, PhotoImage
import os
import sys
import hashlib
import json
from user_auth import register_user, login_user, get_user_data
from file_operations import list_files, upload_file, download_file, delete_file, share_file
from encryption_service import encrypt_file, decrypt_file
from activity_monitor import log_activity, view_activity_logs
from settings import save_settings, load_settings

class FileManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SecureFileX - Secure File Management System")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        # Set icon if available
        try:
            self.root.iconphoto(True, PhotoImage(file="assets/icon.png"))
        except:
            pass
        
        self.current_user = None
        self.current_directory = "files"
        
        # Create necessary directories
        if not os.path.exists("files"):
            os.makedirs("files")
        if not os.path.exists("users"):
            os.makedirs("users")
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        self.show_login_page()
    
    def show_login_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.login_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.login_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
