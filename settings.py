import os
import json
def save_settings(username, settings):
    """Save user settings"""
    users_dir = "users"
    if not os.path.exists(users_dir):
        os.makedirs(users_dir)
