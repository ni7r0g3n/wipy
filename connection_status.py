#!/usr/bin/env python3

from threading import Thread
import time
import subprocess
from pystray import Icon, Menu, MenuItem
from PIL import Image  # Make sure to install the Pillow library

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Function to ping Google and return True if successful, False otherwise
def is_ping_successful():
    try:
        subprocess.check_output(["ping", "-c", "1", "google.com"])
        return True
    except subprocess.CalledProcessError:
        return False

def notify(message, icon):
    subprocess.Popen(['notify-send', message, '-i', icon])
    return

# Function to update the system tray icon based on ping success
def update_icon(icon, previous_status=True):
    if is_ping_successful():
        print(f"{bcolors.OKGREEN} {bcolors.ENDC} Internet OK")
        icon.icon = connected_icon
        icon.title = "Connection status: OK"
        if previous_status == False:
            notify("Internet connection working", "/usr/share/connection_status/internet.ok.png")
            previous_status = True
        # icon.update_menu(Menu(MenuItem('Connected', None)))
    else:
        print(f"{bcolors.FAIL} {bcolors.ENDC} No Internet")
        icon.icon = disconnected_icon
        icon.title = "Connection status: DEAD"
        if previous_status == True:
            notify("No Internet connection available", "/usr/share/connection_status/internet.notok.png")
            previous_status = False
        # icon.update_menu(Menu(MenuItem('Disconnected', None)))
    return previous_status

# Load the icons for connected and disconnected states
connected_icon = Image.open("/usr/share/connection_status/internet.ok.png")
disconnected_icon = Image.open("/usr/share/connection_status/internet.notok.png")

# Create the system tray icon with the connected icon
icon = Icon("Connection Status", connected_icon)

# Set the initial icon based on the first ping result
update_icon(icon)

# Function to periodically update the icon based on ping success
def periodic_update(icon, items):
    status = True
    while True:
        status = update_icon(icon, status)
        time.sleep(2)

# Start the periodic update in a separate thread
update_thread = Thread(target=periodic_update, args=(icon, None))
update_thread.start()

# Run the system tray icon
icon.run()
