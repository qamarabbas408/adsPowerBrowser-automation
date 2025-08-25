# main.py

from automator.adspower_automator import AdsPowerAutomator
import os
import sys
import time
import constants  # Import the new constants file
from helper import generate_dynamic_username,log_profile_to_csv,is_ipv6

def create_single_profile(automator: AdsPowerAutomator):
    """
    This function encapsulates the entire process of creating one profile.
    """
    print("\n--- Starting New Profile Creation ---")
    
    # Click 'New Profile'
    automator.find_and_click(constants.NEW_PROFILE_BUTTON_IMAGE)
    time.sleep(5)
    
    # Set User Agent
    automator.find_and_set_user_agent(
        field_identifier_img=constants.USER_AGENT_ICON_IMAGE,
        user_agents_list=constants.USER_AGENTS,
        click_offset=-150
    )
    
    automator.find_and_click(constants.PROXY_TAB_BUTTON_IMAGE)
    time.sleep(1)

    assigned_ip = None
    profile_accepted = False # A flag to track if we found a good IP

    for attempt in range(constants.PROXY_CHECK_MAX_RETRIES):
        print(f"\n--- Proxy Check Attempt #{attempt}/{constants.PROXY_CHECK_MAX_RETRIES} ---")
        
        automator.find_and_set_host_label(
            field_identifier_img=constants.PROXY_HOST_PORT_LABEL_IMAGE,
            host_label=generate_dynamic_username(constants.HOST_PORT_LABEL),
            click_offset=60 )
        
        time.sleep(2)
        automator.find_and_click(constants.CHECK_PROXY_BUTTON_IMAGE)
        time.sleep(5)

        assigned_ip = automator.get_ip_via_clipboard(
        success_landmark_img=constants.PROXY_SUCCESS_MESSAGE_IMAGE,
        x_offset=20,  # A guess: 20 pixels to the right of the "Connection..." text
        y_offset=25   # A guess: 25 pixels down from the top of the "Connection..." text
    )
        time.sleep(2)
        print("ips generated ==== at attempt",attempt)
        print(assigned_ip)
        
        if assigned_ip and not is_ipv6(assigned_ip): # Assuming you want to keep rejecting IPv6
            print(f"[ACCEPTED] IP '{assigned_ip}' is valid. Logging and saving profile.")
            profile_accepted = True
            break
        else:
            print(f"[REJECTED] IP '{assigned_ip}' is invalid or not found. Cancelling.")
            # automator.find_and_click(constants.CANCEL_BUTTON_IMAGE)
            profile_accepted = False
            continue

        
    if profile_accepted:
        profile_data = {
            'Profile Name': f"AutomatedProfile_{int(time.time())}",
            'Assigned IP': assigned_ip
            }
        log_profile_to_csv(profile_data)

        automator.find_and_click(constants.OK_BUTTON_IMAGE)
        time.sleep(12)

def main():
    """Main function to run the automation script."""

    # Initialize the automator
    automator = AdsPowerAutomator(confidence=0.9)

    try:
        # --- Step 1: Launch the Application ---
        # The script will try to run this first.
        automator.launch_app(constants.APP_PATH)
        automator.wait_for_element(constants.NEW_PROFILE_BUTTON_IMAGE)
        profiles_created_count  = 0 
        while profiles_created_count < constants.TOTAL_PROFILES_TO_CREATE:
            print(f"\n<<<<<<<<<< Starting New Batch. Target: {constants.TOTAL_PROFILES_TO_CREATE * 12} profiles. "
                            f"Completed: {profiles_created_count} >>>>>>>>>>")
           
            # Step 2: Loop to create two profiles
            for i in range(2):
                print(f"\n================ Starting Profile Creation #{i + 1} ================ ")
                create_single_profile(automator)
                profiles_created_count += 1
            print("\n================ Two Profiles Created Successfully ================")
            automator.delete_all_profiles(constants.SELECT_ALL_CHECKBOX_IMAGE,constants.DELETE_ICON_IMAGE,constants.CONFIRM_DELETE_IMAGE)
            time.sleep(8)
    except Exception as e:
        # If either launch_app() or find_and_click() fails, the script will stop
        # and print the error message here.
        print(f"\nAn error occurred during automation: {e}")


if __name__ == "__main__":
    main()