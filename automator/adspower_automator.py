# automator/adspower_automator.py

import pyautogui
import subprocess
import sys
import time
import os
import random

import pyperclip
import pytesseract
import re
from helper import is_ipv6

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class AdsPowerAutomator:
    """
    A class to automate interactions with the AdsPower desktop application.
    """
    def __init__(self, confidence=0.9, wait_time=1.5):
        """
        Initializes the Automator.
        :param confidence: The confidence level for image recognition (from 0.0 to 1.0).
        :param wait_time: Default time in seconds to wait after most actions.
        """
        self.confidence = confidence
        self.wait_time = wait_time
        # Ensure the 'images' directory exists
        if not os.path.exists('images'):
            os.makedirs('images')
        print("AdsPower Automator initialized.")

    def launch_app(self, app_path):
        """
        Launches the application using the specified path.
        This method is OS-aware (Windows/macOS).
        
        :param app_path: The full path to the application executable or .app file.
        """
        print(f"Attempting to launch application from: {app_path}")
        try:
            if sys.platform == "win32": # For Windows
                subprocess.Popen([app_path])
            elif sys.platform == "darwin": # For macOS
                subprocess.Popen(["open", app_path])
            else: # For Linux
                subprocess.Popen([app_path])
                
            print("Application launched. Waiting 10 seconds for it to load...")
            time.sleep(10) # Give the app a generous time to start up
            
        except FileNotFoundError:
            print(f"Error: Application not found at '{app_path}'. Please check the path.")
            raise
        except Exception as e:
            print(f"An unexpected error occurred while launching the app: {e}")
            raise


     # --- NEW ROBUST LOCATE FUNCTION ---
    def locate_on_screen(self, image_path):
        """
        A robust wrapper for pyautogui.locateOnScreen.

        This function searches the screen for a given image and handles the
        case where the image is not found, preventing the script from crashing.

        :param image_path: Path to the screenshot of the element to locate.
        :return: A Box object (left, top, width, height) if found, otherwise None.
        """
        print(f"Searching for image: {image_path}")
        try:
            # Use the confidence level defined when the class was initialized
            location = pyautogui.locateOnScreen(image_path, confidence=self.confidence)
            
            if location:
                print(f"Image found at: {location}")
                return location
            else:
                # This path is taken if the image is not found but doesn't raise an exception
                print(f"Image not found on screen: {image_path}")
                return None

        except pyautogui.ImageNotFoundException:
            # This is the most common way pyautogui signals a failure
            print(f"ImageNotFoundException: Could not locate '{image_path}' on the screen.")
            return None
        except Exception as e:
            # This catches other potential errors, like a corrupted image file
            print(f"An unexpected error occurred while locating '{image_path}': {e}")
            return None
        
    def find_and_click(self, image_path):
        """
        Finds an element on the screen based on an image and clicks its center.
        
        :param image_path: Path to the screenshot of the element to click.
        :return: True if successful, raises an exception otherwise.
        """
        try:
            print(f"Searching for element: {image_path}")
            location = pyautogui.locateCenterOnScreen(image_path, confidence=self.confidence)
            
            if location:
                pyautogui.click(location)
                print(f"Clicked on element: {image_path}")
                time.sleep(self.wait_time)
                return True
            else:
                raise pyautogui.ImageNotFoundException

        except pyautogui.ImageNotFoundException:
            print(f"Fatal Error: Could not locate '{image_path}' on the screen.")
            print("Tip: Make sure the app window is visible and the screenshot is accurate.")
            raise # Stop the script if a critical element is not found
    
    def find_and_click_with_offset(self, image_path, x_offset=0, y_offset=0):
        """
        Finds an element by image, then clicks at an offset from its center.

        :param image_path: Path to the screenshot of the element to find.
        :param x_offset: Pixels to move left (-) or right (+) from the center.
        :param y_offset: Pixels to move up (-) or down (+) from the center.
        :return: True if successful, raises an exception otherwise.
        """
        try:
            print(f"Searching for reference element: {image_path}")
            location = pyautogui.locateCenterOnScreen(image_path, confidence=self.confidence)
            
            if location:
                # Calculate the new click position with the offset
                click_x = location.x + x_offset
                click_y = location.y + y_offset
                
                print(f"Reference found. Clicking at offset position: ({click_x}, {click_y})")
                pyautogui.click(click_x, click_y)
                time.sleep(self.wait_time)
                return True
            else:
                raise pyautogui.ImageNotFoundException

        except pyautogui.ImageNotFoundException:
            print(f"Fatal Error: Could not locate '{image_path}' on the screen.")
            raise

    # NOW, LET'S UPDATE the find_and_set_user_agent method to use our new clicker
    def find_and_set_user_agent(self, field_identifier_img, user_agents_list, click_offset):
        """
        Finds an input field using an identifier image, clicks it at an offset,
        clears it, and types a randomly selected user agent.
        """
        print("\n--- Setting User Agent ---")
        
        # 1. Find the icon and click to the LEFT of it
        self.find_and_click_with_offset(field_identifier_img, x_offset=click_offset)
        
        # 2. Select a random user agent
        random_agent = random.choice(user_agents_list)
        print(f"Selected random user agent: {random_agent[:50]}...")
       

        print("Clearing existing host label...")
        hotkey_command = 'command' if sys.platform == 'darwin' else 'ctrl'
        pyautogui.hotkey(hotkey_command, 'a')
        pyautogui.press('backspace')
        time.sleep(0.5)
        
        # 4. Type the new user agent
        # self.type_text(host_label, interval=0.01)
        # normal typing input doesn't works -- only copy past works 
        pyperclip.copy(random_agent)
        time.sleep(1)

        # 2. Use the "paste" hotkey (Ctrl+V or Cmd+V)
        hotkey_command = 'command' if sys.platform == 'darwin' else 'ctrl'
        pyautogui.hotkey(hotkey_command, 'v')
        print("Paste complete.")
        
        # # 4. Type the new user agent
        # self.type_text(random_agent, interval=0.01)
        
        print("--- User Agent Set Successfully ---")

    # In automator/adspower_automator.py

    def find_and_set_host_label(self, field_identifier_img, host_label, click_offset):
        """
        Finds an input field using an identifier image, clicks it at an offset,
        clears it, and types a randomly selected host label.
        """
        print("\n--- Setting host label ---")
        
        # 1. Find the icon and click to the LEFT of it
        self.find_and_click_with_offset(field_identifier_img, x_offset=click_offset)
        
        # 3. Clear the field
        print("Clearing existing host label...")
        hotkey_command = 'command' if sys.platform == 'darwin' else 'ctrl'
        pyautogui.hotkey(hotkey_command, 'a')
        pyautogui.press('backspace')
        time.sleep(0.5)
        
        # 4. Type the new user agent
        # self.type_text(host_label, interval=0.01)
        # normal typing input doesn't works -- only copy past works 
        pyperclip.copy(host_label)
        # 2. Use the "paste" hotkey (Ctrl+V or Cmd+V)
        hotkey_command = 'command' if sys.platform == 'darwin' else 'ctrl'
        pyautogui.hotkey(hotkey_command, 'v')
        print("Paste complete.")


        print("--- Host Label Set Successfully ---")

    def check_proxy_status(self, check_button_img, success_img, failure_img, wait_seconds=18):
        """
        Clicks the 'Check Proxy' button, waits, and determines the outcome.

        :param check_button_img: Screenshot of the 'Check Proxy' button.
        :param success_img: Screenshot of the success message (e.g., 'Connection test passed!').
        :param failure_img: Screenshot of the failure message (e.g., 'Connection test failed!').
        :param wait_seconds: How long to wait for a result.
        :return: A string: "success", "failure", or "timeout".
        """
        print("\n--- Checking Proxy Status ---")
        
        # 1. Click the 'Check Proxy' button
        self.find_and_click(check_button_img)
        

    def delete_all_profiles(self, select_all_img, delete_icon_img, confirm_delete_img):
        """
        Deletes all profiles by clicking the 'select all' checkbox,
        the delete button, and the final confirmation.
        """
        print("\n--- Deleting All Profiles ---")
        
        # 1. Click the 'Select All' checkbox at the top of the list
        self.find_and_click(select_all_img)
        
        # 2. Click the 'Delete' icon that appears
        self.find_and_click(delete_icon_img)
        
        # 3. Click the final 'Confirm' or 'Delete' button in the pop-up
        self.find_and_click(confirm_delete_img)
        
        print("Deletion command sent. Waiting 10 seconds for profiles to be removed...")
        time.sleep(10)
        print("--- Deletion Process Complete ---")

    def type_text(self, text, interval=0.1):
        """
        Types the given text with a short delay between keystrokes.
        
        :param text: The string to type.
        :param interval: The delay between each keystroke to simulate human typing.
        """
        print(f"Typing: '{'********' if 'pass' in text.lower() else text}'")
        pyautogui.write(text, interval=interval)
        time.sleep(self.wait_time)

  # --- FUNCTION 1: SAVE THE SCREENSHOT ---
    def save_screenshot_of_ip_region(self, success_landmark_img, region_width, region_height):
        """
        Finds the success message landmark and saves a screenshot of the region below it.

        :return: The file path to the saved screenshot, or None if it fails.
        """
        print("\n--- Locating region and saving screenshot ---")
        
        landmark_location = self.locate_on_screen(success_landmark_img)
        if not landmark_location:
            print("Could not find the success landmark to take a screenshot.")
            return None

        # Define the region for the screenshot
        left_coord = int(landmark_location.left)
        top_coord = int(landmark_location.top)
        landmark_height = int(landmark_location.height)
        landmark_width = int(landmark_location.width)
        ocr_region = (left_coord, top_coord, landmark_width+region_width, landmark_height+region_height)
        print(f"Defined screenshot region at: {ocr_region}")

        try:
            # Take the screenshot
            screenshot = pyautogui.screenshot(region=ocr_region)
            
            # Prepare the save directory and filename
            save_dir = os.path.join('images', 'ipaddress')
            os.makedirs(save_dir, exist_ok=True)
            timestamp = int(time.time())
            save_path = os.path.join(save_dir, f"ip_region_{timestamp}.png")
            
            # Save the image file and return the path
            screenshot.save(save_path)
            print(f"Saved IP region screenshot to: {save_path}")
            return save_path

        except Exception as e:
            print(f"An error occurred while saving the screenshot: {e}")
            return None
        
  # --- FUNCTION 2: PERFORM OCR ON A SAVED FILE ---
     # --- REPLACE the old perform_ocr_on_image with this new version ---
    def perform_ocr_on_image(self, image_path):
        """
        Performs OCR on a given image file and intelligently extracts a multi-line IP address.
        """
        print(f"\n--- Performing smart OCR on image: {image_path} ---")
        if not os.path.exists(image_path):
            print(f"OCR failed. File not found at path: {image_path}")
            return None
            
        try:
            raw_text = pytesseract.image_to_string(image_path)
            print("raw text ====",raw_text)

            # --- THE FIX: Convert raw_text to lower case before searching ---
            lower_raw_text = raw_text.lower()
            start = lower_raw_text.find("ip:") # Search for "ip:" in lower case
            end = lower_raw_text.find("country") # Search for "country" in lower case
           
            # start = raw_text.find("IP:")
            # end = raw_text.find("Country")
            if start != -1:
                if end != -1:
                    relevant_text = raw_text[start + len("IP:"):end]
                else:
                    relevant_text = raw_text[start + len("IP:"):]
            else:
                relevant_text = ""

            cleaned = ''.join(relevant_text.split())
            cleaned = cleaned.replace('s', '5').replace('S', '5')

            print(f"Successfully extracted full IP: {cleaned}")
            return cleaned

        except Exception as e:
            print(f"An error occurred during the OCR process: {e}")
            return None
     
    def wait_for_element(self, image_path, timeout=30):
            """
            Waits for a specified element to appear on the screen.
            This is much more reliable than a fixed time.sleep().

            :param image_path: The screenshot of the element to wait for.
            :param timeout: The maximum number of seconds to wait before giving up.
            :return: The location Box object if found, otherwise raises an exception.
            """
            print(f"\n--- Actively waiting for element to appear: {image_path} (Timeout: {timeout}s) ---")
            start_time = time.time()
            while time.time() - start_time < timeout:
                location = self.locate_on_screen(image_path) # Uses our robust, safe locate function
                if location:
                    print("Element found. Proceeding.")
                    return location
                time.sleep(1) # Wait 1 second before checking again
            
            # If the loop finishes, the element was never found
            raise Exception(f"Wait timed out. Element '{image_path}' did not appear on screen after {timeout} seconds.")
    
# --- REPLACE your get_ip_via_clipboard with this corrected version ---
    def get_ip_via_clipboard(self, success_landmark_img, x_offset, y_offset):
        """
        Finds the success message, copies the IP, robustly cleans the "IP:" prefix,
        and returns the full, cleaned IP address.
        """
        print("\n--- Getting IP address via Clipboard (Triple-Click Method) ---")
        
        landmark_location = self.locate_on_screen(success_landmark_img)
        if not landmark_location:
            return None

        click_x = int(landmark_location.left) + x_offset
        click_y = int(landmark_location.top) + y_offset

        try:
            pyautogui.tripleClick(click_x, click_y)
            time.sleep(1) # Reduced sleep time for efficiency

            hotkey = 'command' if sys.platform == 'darwin' else 'ctrl'
            pyautogui.hotkey(hotkey, 'c')
            time.sleep(2)

            ip_from_clipboard = pyperclip.paste().strip()
            
            # --- THIS IS THE CORRECTED LOGIC ---
            # This reliably removes the prefix, whether it's "IP:", "ip:", or "1P:",
            # without damaging the rest of the address.
            if ":" in ip_from_clipboard:
                # We split the string only ONCE at the first colon.
                # The result is a list of two items, e.g., ['IP', '2600:1700...']
                # We take the second item [-1], which is the full address.
                full_ip = ip_from_clipboard.split(':', 1)[-1].strip()
            else:
                # If there's no colon, we assume it's a clean IP.
                full_ip = ip_from_clipboard

            print(f"Retrieved from clipboard: '{ip_from_clipboard}' -> Cleaned IP: '{full_ip}'")
            return full_ip

        except Exception as e:
            print(f"An error occurred during the clipboard operation: {e}")
            return None