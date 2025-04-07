import os
import shutil
import time
import json
from user_auth import get_user_data, add_shared_file
from encryption_service import encrypt_file, decrypt_file
def list_files(username, shared=False):
    """
    List files for a user
    If shared=True, list files shared with the user
    """
    if shared:
        # Get shared files
        user_data = get_user_data(username)
        if not user_data or "shared_with_me" not in user_data:
            return []
        
        shared_files = []
        for shared_file in user_data["shared_with_me"]:
            shared_files.append({
                "name": shared_file["name"],
                "shared_by": shared_file["owner"],
                "date_shared": shared_file["shared_date"]
            })
        
        return shared_files
    else:
        # Get user's own files
        user_dir = os.path.join("files", username)
        if not os.path.exists(user_dir):
            return []
        
        files = []
        for filename in os.listdir(user_dir):
            # Skip metadata files
            if filename.endswith(".meta"):
                continue
                
            file_path = os.path.join(user_dir, filename)
            if os.path.isfile(file_path):
                size_bytes = os.path.getsize(file_path)
                
                # Format size
                if size_bytes < 1024:
                    size = f"{size_bytes} B"
                elif size_bytes < 1024 * 1024:
                    size = f"{size_bytes / 1024:.1f} KB"
                else:
                    size = f"{size_bytes / (1024 * 1024):.1f} MB"
                    
                modified_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(os.path.getmtime(file_path)))
                
                files.append({
                    "name": filename,
                    "size": size,
                    "modified": modified_time
                })
        
        return files
