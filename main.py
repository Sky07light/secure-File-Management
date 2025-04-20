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

def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password")
            return
        
        success, user_data = login_user(username, password)
        
        if success:
            self.current_user = username
            log_activity(username, "Logged in")
            messagebox.showinfo("Success", f"Welcome {user_data.get('fullname', username)}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    
    def register(self):
        fullname = self.fullname_entry.get()
        username = self.reg_username_entry.get()
        email = self.email_entry.get()
        password = self.reg_password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        if not fullname or not username or not email or not password:
            messagebox.showerror("Error", "All fields are required")
            return
            
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
            return
            
        success = register_user(username, password, fullname, email)
        
        if success:
            messagebox.showinfo("Success", "Registration successful! Please login.")
            self.show_login_page()
        else:
            messagebox.showerror("Error", "Username already exists")

def show_dashboard(self):
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Create main application window with sidebar and content area
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sidebar
        self.sidebar = tk.Frame(self.main_frame, bg="#2c3e50", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)
        
        # User info
        user_data = get_user_data(self.current_user)
        user_frame = tk.Frame(self.sidebar, bg="#2c3e50", pady=20)
        user_frame.pack(fill=tk.X)
        
        tk.Label(user_frame, text=f"Welcome,", font=("Helvetica", 10), bg="#2c3e50", fg="#ecf0f1").pack()
        tk.Label(user_frame, text=f"{user_data.get('fullname', self.current_user)}", 
                 font=("Helvetica", 12, "bold"), bg="#2c3e50", fg="#ecf0f1").pack()
        
        # Navigation menu
        menu_frame = tk.Frame(self.sidebar, bg="#2c3e50", pady=20)
        menu_frame.pack(fill=tk.X)
        
        buttons = [
            ("My Files", self.show_files_page),
            ("Upload File", self.show_upload_page),
            ("Shared Files", self.show_shared_page),
            ("Activity Logs", self.show_logs_page),
            ("Settings", self.show_settings_page),
            ("Logout", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(menu_frame, text=text, command=command, font=("Helvetica", 11),
                         bg="#34495e", fg="#ecf0f1", bd=0, width=20, pady=8, anchor="w", padx=15)
            btn.pack(fill=tk.X, pady=3)
        
        # Content area
        self.content_frame = tk.Frame(self.main_frame, bg="#ecf0f1")
        self.content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Show files page by default
        self.show_files_page()
    
    def show_files_page(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Page header
        header_frame = tk.Frame(self.content_frame, bg="#ecf0f1", pady=15, padx=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="My Files", font=("Helvetica", 18, "bold"), bg="#ecf0f1").pack(side=tk.LEFT)
        
        # File listing
        list_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # File headers
        headers_frame = tk.Frame(list_frame, bg="#f5f5f5")
        headers_frame.pack(fill=tk.X, pady=5)
        
        headers = ["Filename", "Size", "Date Modified", "Actions"]
        widths = [3, 1, 2, 2]
        
        for i, header in enumerate(headers):
            tk.Label(headers_frame, text=header, font=("Helvetica", 11, "bold"), 
                    bg="#f5f5f5", pady=8, padx=10).grid(row=0, column=i, sticky="w", padx=5)
            headers_frame.grid_columnconfigure(i, weight=widths[i])

# Get files
        files = list_files(self.current_user)
        
        if not files:
            tk.Label(list_frame, text="No files found. Upload some files to get started!",
                    font=("Helvetica", 12), fg="#555", bg="white", pady=30).pack()
        else:
            files_canvas = tk.Canvas(list_frame, bg="white")
            files_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL, command=files_canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            files_canvas.configure(yscrollcommand=scrollbar.set)
            files_canvas.bind('<Configure>', lambda e: files_canvas.configure(scrollregion=files_canvas.bbox("all")))
            
            files_frame = tk.Frame(files_canvas, bg="white")
            files_canvas.create_window((0, 0), window=files_frame, anchor="nw")
            
            for i, file_info in enumerate(files):
                bg_color = "#f9f9f9" if i % 2 == 0 else "white"
                row_frame = tk.Frame(files_frame, bg=bg_color)
                row_frame.pack(fill=tk.X)
                
                tk.Label(row_frame, text=file_info["name"], font=("Helvetica", 11), bg=bg_color, 
                        pady=10, padx=10).grid(row=0, column=0, sticky="w", padx=5)
                
                tk.Label(row_frame, text=file_info["size"], font=("Helvetica", 11), bg=bg_color,
                        pady=10).grid(row=0, column=1, sticky="w", padx=5)
                
                tk.Label(row_frame, text=file_info["modified"], font=("Helvetica", 11), bg=bg_color,
                        pady=10).grid(row=0, column=2, sticky="w", padx=5)
                
                actions_frame = tk.Frame(row_frame, bg=bg_color)
                actions_frame.grid(row=0, column=3, sticky="w", padx=5)
                
                tk.Button(actions_frame, text="Download", font=("Helvetica", 10),
                         bg="#3498db", fg="white", bd=0, padx=8, pady=2,
                         command=lambda f=file_info["name"]: self.download_file(f)).pack(side=tk.LEFT, padx=5)
                
                tk.Button(actions_frame, text="Share", font=("Helvetica", 10),
                         bg="#2ecc71", fg="white", bd=0, padx=8, pady=2,
                         command=lambda f=file_info["name"]: self.show_share_dialog(f)).pack(side=tk.LEFT, padx=5)
                
                tk.Button(actions_frame, text="Delete", font=("Helvetica", 10),
                         bg="#e74c3c", fg="white", bd=0, padx=8, pady=2,
                         command=lambda f=file_info["name"]: self.delete_file(f)).pack(side=tk.LEFT, padx=5)
                
                for j in range(4):
                    row_frame.grid_columnconfigure(j, weight=widths[j])

def show_upload_page(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Page header
        header_frame = tk.Frame(self.content_frame, bg="#ecf0f1", pady=15, padx=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Upload File", font=("Helvetica", 18, "bold"), bg="#ecf0f1").pack(side=tk.LEFT)
        
        # Upload section
        upload_frame = tk.Frame(self.content_frame, bg="white", padx=30, pady=40)
        upload_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # File input
        tk.Label(upload_frame, text="Select a file to upload:", font=("Helvetica", 12, "bold"), 
                bg="white", anchor="w").pack(fill=tk.X, pady=(0, 10))
        
        file_path_frame = tk.Frame(upload_frame, bg="white")
        file_path_frame.pack(fill=tk.X, pady=10)
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_path_frame, textvariable=self.file_path_var, font=("Helvetica", 11), width=50)
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_button = tk.Button(file_path_frame, text="Browse", command=self.browse_file, 
                                 font=("Helvetica", 11), bg="#3498db", fg="white")
        browse_button.pack(side=tk.RIGHT)
        
        # Encryption options
        encrypt_frame = tk.Frame(upload_frame, bg="white", pady=20)
        encrypt_frame.pack(fill=tk.X)
        
        tk.Label(encrypt_frame, text="Security Options:", font=("Helvetica", 12, "bold"), 
                bg="white", anchor="w").pack(fill=tk.X, pady=(0, 10))
        
        self.encrypt_var = tk.BooleanVar(value=True)
        encrypt_check = tk.Checkbutton(encrypt_frame, text="Encrypt file", variable=self.encrypt_var, 
                                      font=("Helvetica", 11), bg="white")
        encrypt_check.pack(anchor="w")
# Upload button
        button_frame = tk.Frame(upload_frame, bg="white", pady=20)
        button_frame.pack(fill=tk.X)
        
        upload_btn = tk.Button(button_frame, text="Upload File", command=self.upload_file,
                              font=("Helvetica", 12, "bold"), bg="#27ae60", fg="white", padx=20, pady=10)
        upload_btn.pack()
    
    def show_shared_page(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Page header
        header_frame = tk.Frame(self.content_frame, bg="#ecf0f1", pady=15, padx=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Shared Files", font=("Helvetica", 18, "bold"), bg="#ecf0f1").pack(side=tk.LEFT)
        
        # Shared files content
        shared_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        shared_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Get shared files
        shared_files = list_files(self.current_user, shared=True)
        
        if not shared_files:
            tk.Label(shared_frame, text="No shared files available.",
                    font=("Helvetica", 12), fg="#555", bg="white", pady=30).pack()
        else:
            # File headers
            headers_frame = tk.Frame(shared_frame, bg="#f5f5f5")
            headers_frame.pack(fill=tk.X, pady=5)
            
            headers = ["Filename", "Shared By", "Date Shared", "Actions"]
            widths = [3, 2, 2, 1]
            
            for i, header in enumerate(headers):
                tk.Label(headers_frame, text=header, font=("Helvetica", 11, "bold"), 
                        bg="#f5f5f5", pady=8, padx=10).grid(row=0, column=i, sticky="w", padx=5)
                headers_frame.grid_columnconfigure(i, weight=widths[i])
            
            # File list
            for i, file in enumerate(shared_files):
                bg_color = "#f9f9f9" if i % 2 == 0 else "white"
                row_frame = tk.Frame(shared_frame, bg=bg_color)
                row_frame.pack(fill=tk.X)
                
                tk.Label(row_frame, text=file["name"], font=("Helvetica", 11), bg=bg_color, 
                        pady=10, padx=10).grid(row=0, column=0, sticky="w", padx=5)
                
                tk.Label(row_frame, text=file["shared_by"], font=("Helvetica", 11), bg=bg_color,
                        pady=10).grid(row=0, column=1, sticky="w", padx=5)
                
                tk.Label(row_frame, text=file["date_shared"], font=("Helvetica", 11), bg=bg_color,
                        pady=10).grid(row=0, column=2, sticky="w", padx=5)
                
                tk.Button(row_frame, text="Download", font=("Helvetica", 10),
                         bg="#3498db", fg="white", bd=0, padx=10, pady=3,
                         command=lambda f=file["name"], u=file["shared_by"]: self.download_shared_file(f, u)).grid(row=0, column=3, padx=5)
                
                for j in range(4):
                    row_frame.grid_columnconfigure(j, weight=widths[j])
    
    def show_logs_page(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Page header
        header_frame = tk.Frame(self.content_frame, bg="#ecf0f1", pady=15, padx=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Activity Logs", font=("Helvetica", 18, "bold"), bg="#ecf0f1").pack(side=tk.LEFT)
        
        # Activity logs content
        logs_frame = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        logs_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Get logs
        logs = view_activity_logs(self.current_user)
        
        if not logs:
            tk.Label(logs_frame, text="No activity logs found.",
                    font=("Helvetica", 12), fg="#555", bg="white", pady=30).pack()
        else:
            # Log headers
            headers_frame = tk.Frame(logs_frame, bg="#f5f5f5")
            headers_frame.pack(fill=tk.X, pady=5)
            
            headers = ["Timestamp", "Activity", "Details"]
            widths = [2, 2, 4]
            
            for i, header in enumerate(headers):
                tk.Label(headers_frame, text=header, font=("Helvetica", 11, "bold"), 
                        bg="#f5f5f5", pady=8, padx=10).grid(row=0, column=i, sticky="w", padx=5)
                headers_frame.grid_columnconfigure(i, weight=widths[i])
            
            # Log entries
            logs_canvas = tk.Canvas(logs_frame, bg="white")
            logs_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            scrollbar = tk.Scrollbar(logs_frame, orient=tk.VERTICAL, command=logs_canvas.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            logs_canvas.configure(yscrollcommand=scrollbar.set)
            logs_canvas.bind('<Configure>', lambda e: logs_canvas.configure(scrollregion=logs_canvas.bbox("all")))
            
            inner_frame = tk.Frame(logs_canvas, bg="white")
            logs_canvas.create_window((0, 0), window=inner_frame, anchor="nw")
            
            for i, log in enumerate(logs):
                bg_color = "#f9f9f9" if i % 2 == 0 else "white"
                row_frame = tk.Frame(inner_frame, bg=bg_color)
                row_frame.pack(fill=tk.X)
                
                tk.Label(row_frame, text=log["timestamp"], font=("Helvetica", 11), bg=bg_color, 
                        pady=10, padx=10, wraplength=150).grid(row=0, column=0, sticky="w", padx=5)
                
                tk.Label(row_frame, text=log["activity"], font=("Helvetica", 11), bg=bg_color,
                        pady=10, wraplength=150).grid(row=0, column=1, sticky="w", padx=5)
                
                tk.Label(row_frame, text=log["details"], font=("Helvetica", 11), bg=bg_color,
                        pady=10, wraplength=300).grid(row=0, column=2, sticky="w", padx=5)
                
                for j in range(3):
                    row_frame.grid_columnconfigure(j, weight=widths[j])
    
    def show_settings_page(self):
        # Clear content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()
            
        # Page header
        header_frame = tk.Frame(self.content_frame, bg="#ecf0f1", pady=15, padx=20)
        header_frame.pack(fill=tk.X)
        
        tk.Label(header_frame, text="Settings", font=("Helvetica", 18, "bold"), bg="#ecf0f1").pack(side=tk.LEFT)
        
        # Settings content
        settings_frame = tk.Frame(self.content_frame, bg="white", padx=30, pady=30)
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Load user settings
        user_settings = load_settings(self.current_user)
        
        # Security settings
        security_frame = tk.Frame(settings_frame, bg="white", pady=10)
        security_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(security_frame, text="Security Settings", font=("Helvetica", 14, "bold"), bg="white").pack(anchor="w")
        
        self.auto_encrypt = tk.BooleanVar(value=user_settings.get("auto_encrypt", True))
        encrypt_check = tk.Checkbutton(security_frame, text="Automatically encrypt all uploaded files", 
                                      variable=self.auto_encrypt, font=("Helvetica", 11), bg="white")
        encrypt_check.pack(anchor="w", pady=5)
        
        self.two_factor = tk.BooleanVar(value=user_settings.get("two_factor", False))
        two_factor_check = tk.Checkbutton(security_frame, text="Enable two-factor authentication (Coming soon)", 
                                         variable=self.two_factor, font=("Helvetica", 11), bg="white")
        two_factor_check.pack(anchor="w", pady=5)
        
        # Display settings
        display_frame = tk.Frame(settings_frame, bg="white", pady=10)
        display_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(display_frame, text="Display Settings", font=("Helvetica", 14, "bold"), bg="white").pack(anchor="w")
        
        self.show_thumbnails = tk.BooleanVar(value=user_settings.get("show_thumbnails", True))
        thumbnails_check = tk.Checkbutton(display_frame, text="Show file thumbnails", 
                                         variable=self.show_thumbnails, font=("Helvetica", 11), bg="white")
        thumbnails_check.pack(anchor="w", pady=5)
        
        self.dark_mode = tk.BooleanVar(value=user_settings.get("dark_mode", False))
        dark_mode_check = tk.Checkbutton(display_frame, text="Dark mode (Coming soon)", 
                                        variable=self.dark_mode, font=("Helvetica", 11), bg="white")
        dark_mode_check.pack(anchor="w", pady=5)
        
        # Account settings
        account_frame = tk.Frame(settings_frame, bg="white", pady=10)
        account_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(account_frame, text="Account Settings", font=("Helvetica", 14, "bold"), bg="white").pack(anchor="w")
        
        change_pass_btn = tk.Button(account_frame, text="Change Password", font=("Helvetica", 11),
                                   bg="#3498db", fg="white", padx=10, pady=5)
        change_pass_btn.pack(anchor="w", pady=10)
        
        # Save button
        save_frame = tk.Frame(settings_frame, bg="white", pady=20)
        save_frame.pack(fill=tk.X, pady=10)
        
        save_settings_btn = tk.Button(save_frame, text="Save Settings", command=self.save_user_settings,
                                     font=("Helvetica", 12), bg="#27ae60", fg="white", padx=15, pady=8)
        save_settings_btn.pack()
    
    def save_user_settings(self):
        settings = {
            "auto_encrypt": self.auto_encrypt.get(),
            "two_factor": self.two_factor.get(),
            "show_thumbnails": self.show_thumbnails.get(),
            "dark_mode": self.dark_mode.get()
        }
        
        save_settings(self.current_user, settings)
        messagebox.showinfo("Success", "Settings saved successfully!")
    
    def browse_file(self):
        from tkinter import filedialog
        filename = filedialog.askopenfilename(title="Select a file")
        if filename:
            self.file_path_var.set(filename)
    
    def upload_file(self):
        file_path = self.file_path_var.get()
        
        if not file_path:
            messagebox.showerror("Error", "Please select a file to upload")
            return
        
        encrypt = self.encrypt_var.get()
        
        success = upload_file(file_path, self.current_user, encrypt)
        
        if success:
            messagebox.showinfo("Success", "File uploaded successfully!")
            log_activity(self.current_user, "Upload", f"Uploaded file: {os.path.basename(file_path)}")
            self.show_files_page()
        else:
            messagebox.showerror("Error", "Failed to upload file")
    
    def download_file(self, filename):
        from tkinter import filedialog
        save_path = filedialog.asksaveasfilename(title="Save file as", initialfile=filename)
        
        if not save_path:
            return
        
        success = download_file(filename, self.current_user, save_path)
        
        if success:
            messagebox.showinfo("Success", "File downloaded successfully!")
            log_activity(self.current_user, "Download", f"Downloaded file: {filename}")
        else:
            messagebox.showerror("Error", "Failed to download file")
    
    def download_shared_file(self, filename, owner):
        from tkinter import filedialog
        save_path = filedialog.asksaveasfilename(title="Save file as", initialfile=filename)
        
        if not save_path:
            return
        
        success = download_file(filename, owner, save_path, shared_with=self.current_user)
        
        if success:
            messagebox.showinfo("Success", "File downloaded successfully!")
            log_activity(self.current_user, "Download", f"Downloaded shared file: {filename} from {owner}")
        else:
            messagebox.showerror("Error", "Failed to download file")
    
    def delete_file(self, filename):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {filename}?")
        
        if not confirm:
            return
        
        success = delete_file(filename, self.current_user)
        
        if success:
            messagebox.showinfo("Success", "File deleted successfully!")
            log_activity(self.current_user, "Delete", f"Deleted file: {filename}")
            self.show_files_page()
        else:
            messagebox.showerror("Error", "Failed to delete file")
    
    def show_share_dialog(self, filename):
        # Create a new toplevel window
        share_window = tk.Toplevel(self.root)
        share_window.title("Share File")
        share_window.geometry("400x250")
        share_window.configure(bg="white")
        
        # Set modal behavior
        share_window.transient(self.root)
        share_window.grab_set()
        
        # Content
        tk.Label(share_window, text="Share File", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)
        
        tk.Label(share_window, text=f"Filename: {filename}", font=("Helvetica", 12), bg="white").pack(pady=10)
        
        tk.Label(share_window, text="Share with username:", font=("Helvetica", 12), bg="white").pack(pady=5)
        
        username_entry = tk.Entry(share_window, font=("Helvetica", 12), width=30)
        username_entry.pack(pady=10)
        
        def share():
            share_with = username_entry.get()
            
            if not share_with:
                messagebox.showerror("Error", "Please enter a username")
                return
            
            success = share_file(filename, self.current_user, share_with)
            
            if success:
                messagebox.showinfo("Success", f"File shared with {share_with} successfully!")
                log_activity(self.current_user, "Share", f"Shared file: {filename} with {share_with}")
                share_window.destroy()
            else:
                messagebox.showerror("Error", "Failed to share file. User may not exist.")
        
        tk.Button(share_window, text="Share", command=share, font=("Helvetica", 12),
                 bg="#27ae60", fg="white", padx=15, pady=5).pack(pady=15)
    
    def logout(self):
        log_activity(self.current_user, "Logout")
        self.current_user = None
        messagebox.showinfo("Logout", "You have been logged out")
        self.show_login_page()


def main():
    root = tk.Tk()
    app = FileManagementApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
