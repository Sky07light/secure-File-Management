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
def upload_file(source_path, username, encrypt=True):
    """Upload a file to user's directory"""
    try:
        # Create user directory if it doesn't exist
        user_dir = os.path.join("files", username)
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)
        
        # Get filename from path
        filename = os.path.basename(source_path)
        destination_path = os.path.join(user_dir, filename)
        
        # Copy file
        shutil.copy2(source_path, destination_path)
        
        # Encrypt if requested
        if encrypt:
            encrypt_file(destination_path)
            
            # Create metadata file to indicate encryption
            meta_file = f"{destination_path}.meta"
            with open(meta_file, 'w') as f:
                json.dump({"encrypted": True, "uploaded": time.strftime("%Y-%m-%d %H:%M:%S")}, f)
        
        return True
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        return False

def download_file(filename, username, save_path, shared_with=None):
    """Download a file from user's directory or shared file"""
    try:
        # Determine file path based on ownership
        if shared_with:
            # This is a shared file being accessed by shared_with user
            file_owner = username  # In this case, username is the owner
            source_path = os.path.join("files", file_owner, filename)
        else:
            # User is downloading their own file
            source_path = os.path.join("files", username, filename)
        
        if not os.path.exists(source_path):
            return False
            
        # Check if file is encrypted
        is_encrypted = False
        meta_file = f"{source_path}.meta"
        if os.path.exists(meta_file):
            with open(meta_file, 'r') as f:
                metadata = json.load(f)
                is_encrypted = metadata.get("encrypted", False)
        
        # Copy file to temporary location
        temp_path = f"{source_path}.temp"
        shutil.copy2(source_path, temp_path)
        
        # Decrypt if needed
        if is_encrypted:
            decrypt_file(temp_path)
            
        # Move to final destination
        shutil.move(temp_path, save_path)
        return True
    except Exception as e:
        print(f"Error downloading file: {str(e)}")
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return False

def delete_file(filename, username):
    """Delete a file from user's directory"""
    try:
        file_path = os.path.join("files", username, filename)
        meta_file = f"{file_path}.meta"
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        if os.path.exists(meta_file):
            os.remove(meta_file)
            
        return True
    except Exception as e:
        print(f"Error deleting file: {str(e)}")
        return False

def share_file(filename, owner, share_with):
    """Share a file with another user"""
    try:
        # Check if file exists
        file_path = os.path.join("files", owner, filename)
        if not os.path.exists(file_path):
            return False
            
        # Add shared file information to target user
        return add_shared_file(owner, filename, share_with)
    except Exception as e:
        print(f"Error sharing file: {str(e)}")
        return False
