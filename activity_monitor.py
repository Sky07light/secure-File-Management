import os
import json
import time

def log_activity(username, activity, details=""):
    """Log user activity"""
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    user_log_file = os.path.join(logs_dir, f"{username}_activity.log")
    
    # Create log entry
    log_entry = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "activity": activity,
        "details": details,
        "ip_address": "127.0.0.1"  # For demo purposes
    }
    logs = []
    if os.path.exists(user_log_file):
        try:
            with open(user_log_file, 'r') as f:
                logs = json.load(f)
        except:
            logs = []
    
    # Add new log
    logs.append(log_entry)
    
    # Save logs
    with open(user_log_file, 'w') as f:
        json.dump(logs, f, indent=4)
    
    return True

def view_activity_logs(username):
    """Get activity logs for a user"""
    log_file = os.path.join("logs", f"{username}_activity.log")
    
    if not os.path.exists(log_file):
        return []
    
    try:
        with open(log_file, 'r') as f:
            logs = json.load(f)
            # Return most recent logs first
            return sorted(logs, key=lambda x: x["timestamp"], reverse=True)
    except Exception as e:
        print(f"Error reading log file: {str(e)}")
        return []

