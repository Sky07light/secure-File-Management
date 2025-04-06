import os
import json
def save_settings(username, settings):
    """Save user settings"""
    users_dir = "users"
    if not os.path.exists(users_dir):
        os.makedirs(users_dir)
    settings_file = os.path.join(users_dir, f"{username}_settings.json")
    
    # Save settings
    with open(settings_file, 'w') as f:
        json.dump(settings, f, indent=4)
    
    return True
def load_settings(username):
    """Load user settings"""
    settings_file = os.path.join("users", f"{username}_settings.json")
    
    if not os.path.exists(settings_file):
        # Default settings
        return {
            "auto_encrypt": True,
            "two_factor": False,
            "show_thumbnails": True,
            "dark_mode": False
        }
        
    
