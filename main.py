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

title_label = tk.Label(self.login_frame, text="SecureFileX", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333333")
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(self.login_frame, text="Secure File Management System", font=("Helvetica", 14), bg="#f0f0f0", fg="#555555")
        subtitle_label.pack(pady=10)
        

        form_frame = tk.Frame(self.login_frame, bg="#f0f0f0")
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Username:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=10)
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        self.username_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Password:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=10)
        self.password_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=10, padx=10)
        
        button_frame = tk.Frame(self.login_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        login_button = tk.Button(button_frame, text="Login", command=self.login, font=("Helvetica", 12), 
                                bg="#4CAF50", fg="white", width=10)
        login_button.grid(row=0, column=0, padx=10)
        
        register_button = tk.Button(button_frame, text="Register", command=self.show_register_page, font=("Helvetica", 12),
                                   bg="#2196F3", fg="white", width=10)
        register_button.grid(row=0, column=1, padx=10)
        
        # Footer
        footer_frame = tk.Frame(self.login_frame, bg="#f0f0f0")
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)
        
        footer_text = tk.Label(footer_frame, text="B.Tech CSE Project - Operating Systems", 
                              font=("Helvetica", 10), bg="#f0f0f0", fg="#777777")
        footer_text.pack()
    
    def show_register_page(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
        self.register_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.register_frame.pack(fill=tk.BOTH, expand=True, padx=50, pady=50)
   -     
        title_label = tk.Label(self.register_frame, text="Create Account", font=("Helvetica", 24, "bold"), bg="#f0f0f0", fg="#333333")
        title_label.pack(pady=20)

 # this is the registration form
        form_frame = tk.Frame(self.register_frame, bg="#f0f0f0")
        form_frame.pack(pady=20)
        
        tk.Label(form_frame, text="Full Name:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w", pady=10)
        self.fullname_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        self.fullname_entry.grid(row=0, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Username:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="w", pady=10)
        self.reg_username_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        self.reg_username_entry.grid(row=1, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Email:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=10)
        self.email_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30)
        self.email_entry.grid(row=2, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Password:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=3, column=0, sticky="w", pady=10)
        self.reg_password_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30, show="*")
        self.reg_password_entry.grid(row=3, column=1, pady=10, padx=10)
        
        tk.Label(form_frame, text="Confirm Password:", font=("Helvetica", 12), bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=10)
        self.confirm_password_entry = tk.Entry(form_frame, font=("Helvetica", 12), width=30, show="*")
        self.confirm_password_entry.grid(row=4, column=1, pady=10, padx=10)
        
        # Buttons
        button_frame = tk.Frame(self.register_frame, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        register_button = tk.Button(button_frame, text="Register", command=self.register, font=("Helvetica", 12), 
                                   bg="#4CAF50", fg="white", width=10)
        register_button.grid(row=0, column=0, padx=10)
        
        back_button = tk.Button(button_frame, text="Back to Login", command=self.show_login_page, font=("Helvetica", 12),
                               bg="#607D8B", fg="white", width=12)
        back_button.grid(row=0, column=1, padx=10)
