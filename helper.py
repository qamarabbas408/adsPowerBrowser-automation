# helper.py
# This file contains helper functions for data manipulation.

import random
import string
import os
import datetime
import csv
from datetime import datetime

def is_ipv6(ip_string: str) -> bool:
    """Checks if the given string contains colons, indicating an IPv6 format."""
    return ":" in ip_string

def generate_dynamic_username(user_template: str) -> str:
    """
    Takes a username template, finds the 'sessid' part, and replaces
    the following value with a new random string of digits.

    :param user_template: The username part of the proxy string.
    :return: The new username with the randomized session ID.
    :raises ValueError: If 'sessid-' is not found in the template.
    """
    # 1. Generate the random session ID
    random_length = random.randint(10, 25)
    new_session_id = "".join(random.choices(string.digits, k=random_length))
    print(f"Helper function generated new session ID: {new_session_id}")

    # 2. Reconstruct the username
    user_parts = user_template.split('-')
    try:
        # Find the index of 'sessid' and replace the part right after it
        sessid_index = user_parts.index('sessid')
        user_parts[sessid_index + 1] = new_session_id
        final_username = "-".join(user_parts)
        return final_username
    except (ValueError, IndexError):
        # Raise a specific error if the template is malformed
        raise ValueError("Could not find 'sessid-' in the username part of the template string.")
    
def log_profile_to_csv(profile_data: dict):
    """
    Appends a dictionary of profile data to a CSV file inside the 'ipslist' folder.
    The CSV filename is timestamped for the day.
    """
    # --- THIS IS THE MODIFIED PART ---

    # 1. Define the target directory name.
    target_directory = "ipslist"
    
    # 2. Create the directory if it doesn't exist. This is a safe operation.
    os.makedirs(target_directory, exist_ok=True)
    
    # 3. Create the full file path by joining the directory and the filename.
    timestamp = datetime.now().strftime("%Y-%m-%d")
    # os.path.join is the correct way to build paths for any OS.
    filename = os.path.join(target_directory, f"created_profiles_{timestamp}.csv")

    # --- THE REST OF THE FUNCTION IS THE SAME ---

    headers = ['Profile Name','Assigned IP']
    
    file_exists = os.path.exists(filename)
    
    with open(filename, 'a+', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(profile_data)
    
    print(f"\n[SUCCESS] Profile data has been appended to the file: {filename}")
    print(f"Logged data: {profile_data}")