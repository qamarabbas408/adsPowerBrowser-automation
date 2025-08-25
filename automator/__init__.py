# main.py

from automator.adspower_automator import AdsPowerAutomator
import os
import time

def main():
    """Main function to run the automation script."""
    print("Starting AdsPower automation script.")
    print("Please ensure the AdsPower application is open and visible.")
    time.sleep(3) # Gives you time to switch to the app window

    # --- CONFIGURATION ---
    # Create a folder named 'images' in your project directory.
    # You must take screenshots of the UI elements and save them here.
    # Be sure the filenames match what's written below.
    
    IMAGES_DIR = "images"
    USERNAME_IMAGE = os.path.join(IMAGES_DIR, "adspower_username.png")
    PASSWORD_IMAGE = os.path.join(IMAGES_DIR, "adspower_password.png")
    LOGIN_BUTTON_IMAGE = os.path.join(IMAGES_DIR, "adspower_login_button.png")
    
    # --- IMPORTANT: Store credentials securely in a real project ---
    # For this example, we'll define them here.
    ADSPOWER_USER = "your_username_here"
    ADSPOWER_PASS = "your_password_here"

    # Initialize the automator
    automator = AdsPowerAutomator()

    # Execute the login process
    automator.perform_login(
        username_img=USERNAME_IMAGE,
        password_img=PASSWORD_IMAGE,
        login_btn_img=LOGIN_BUTTON_IMAGE,
        username=ADSPOWER_USER,
        password=ADSPOWER_PASS
    )

if __name__ == "__main__":
    # This ensures the script runs only when executed directly
    main()