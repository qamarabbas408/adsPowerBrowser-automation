# constants.py
# A central file for storing all constants and configuration settings.

import os
import sys

# --- APPLICATION PATH ---
# IMPORTANT: You must edit this path to match your system's installation location.
ADSPOWER_APP_PATH_WINDOWS = "C:\Program Files\AdsPower Global\AdsPower Global.exe"
ADSPOWER_APP_PATH_MACOS = "/Applications/AdsPower.app"

# Automatically select the correct path based on the operating system
APP_PATH = ADSPOWER_APP_PATH_WINDOWS if sys.platform == "win32" else ADSPOWER_APP_PATH_MACOS


# --- IMAGE DIRECTORY ---
IMAGES_DIR = "images"


# --- IMAGE FILE PATHS ---
# Login Screen
USERNAME_IMAGE = os.path.join(IMAGES_DIR, "adspower_username.png")
PASSWORD_IMAGE = os.path.join(IMAGES_DIR, "adspower_password.png")
LOGIN_BUTTON_IMAGE = os.path.join(IMAGES_DIR, "adspower_login_button.png")

# Dashboard
NEW_PROFILE_BUTTON_IMAGE = os.path.join(IMAGES_DIR, "new_profile_button.png")


# --- CREDENTIALS ---
# WARNING: For real-world use, store these securely (e.g., environment variables), not in the code.
ADSPOWER_USER = "your_email@example.com"
ADSPOWER_PASS = "YourPassword"


# --- NEW: USER AGENT LIST ---
USER_AGENTS = [
"Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (iPhone; CPU iPhone OS 17_1_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/123.4 Mobile/15E148 Safari/605.1.15",
"Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/124.0.6367.88 Mobile/15E148 Safari/604.1",
"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 10; HD1913) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36 EdgA/122.0.2365.76",
"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.118 Mobile Safari/537.36",
"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.79 Safari/537.36",
"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.60 Safari/537.36",
]
HOST_PORT_LABEL = 'pr.oxylabs.io:7777:customer-TeamAmb_RnjHh-cc-us-sessid-0230170104-sesstime-15:13th_April2025'

USER_AGENT_ICON_IMAGE = os.path.join(IMAGES_DIR, "user_agent_icon.png")
USER_AGENT_FIELD_IMAGE = os.path.join(IMAGES_DIR, "user_agent_field.png")
PROXY_TAB_BUTTON_IMAGE = os.path.join(IMAGES_DIR, "proxy_tab_button.png")
PROXY_HOST_PORT_LABEL_IMAGE = os.path.join(IMAGES_DIR, "proxy_host_port_label.png")
CHECK_PROXY_BUTTON_IMAGE = os.path.join(IMAGES_DIR, "check_proxy_button.png")
PROXY_SUCCESS_MESSAGE_IMAGE = os.path.join(IMAGES_DIR, "check_proxy_success.png")
PROXY_FAILURE_MESSAGE_IMAGE = os.path.join(IMAGES_DIR, "check_proxy_failed.png")
OK_BUTTON_IMAGE = os.path.join(IMAGES_DIR, "ok_profile_button.png")
SELECT_ALL_CHECKBOX_IMAGE = os.path.join(IMAGES_DIR, "select_all_checkbox.png")
DELETE_ICON_IMAGE = os.path.join(IMAGES_DIR, "delete_button.png")
CONFIRM_DELETE_IMAGE = os.path.join(IMAGES_DIR, "confirm_button.png")
CANCEL_BUTTON_IMAGE = os.path.join(IMAGES_DIR, "cancel_button.png")
PROXY_CHECK_MAX_RETRIES = 15 # The number of times to try getting a valid IP before giving up
TOTAL_PROFILES_TO_CREATE = 25