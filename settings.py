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
    
