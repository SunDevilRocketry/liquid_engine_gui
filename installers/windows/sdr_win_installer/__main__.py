#Standard Library imports
import sys
import os
from pathlib import Path

from tkinter import *
from tkinter import ttk

# Standardized window creator, just to make sure window geometry is consistent between both version
def create_root_window():
    root_window = Tk()
    root_window.geometry("400x300")

    return root_window

def please_uninstall(installer_root_window):
    # Frame with message to uninstall previously-existing SDEC before installing new version
    please_uninstall_frame = ttk.Frame(installer_root_window, padding=10)
    please_uninstall_frame.grid()

    #Welcome Text
    please_uninstall_text = "An existing installation of the Sun Devil Rocketry Liquid Engine GUI and SDEC has been detected. Please uninstall them before running the installer."
    please_uninstall_label = ttk.Label(please_uninstall_frame, text=please_uninstall_text, wraplength=380)
    please_uninstall_label.grid(column=0, row=0)

def installer_page_1(installer_root_window):
    # Frame with the first installer page
    welcome_frame = ttk.Frame(installer_root_window, padding=10)
    welcome_frame.grid()

    #Welcome Text
    welcome_text = "Welcome to the Sun Devil Rocketry Liquid Engine GUI and SDEC installer for Windows.\n\nPlease choose one of the options below to begin the installation:"
    welcome_label = ttk.Label(welcome_frame, text=welcome_text, wraplength=380)
    welcome_label.grid(column=0, row=0)

    # System-wide Installation Button
    system_installation_button = ttk.Button(welcome_frame, text="System-Wide Installation")
    system_installation_button.grid(column=0, row=1)

    # User installation Button
    user_installation_button = ttk.Button(welcome_frame, text="User Installation")
    user_installation_button.grid(column = 0, row=2)

# Function for running the Windows installation
def installer(admin_access):
    print("Starting installation")
    installer_root_window = create_root_window()

    # Check if there is an existing installation of SDEC
    if not Path("C:/Program Files/Sun Devil Rocketry").exists() and not Path(os.path.expandvars("$APPDATA") + "/Sun Devil Rocketry").exists():
        installer_page_1(installer_root_window)
    else:
        please_uninstall(installer_root_window)

    installer_root_window.mainloop()

def uninstaller():
    uninstaller_root_window = create_root_window()

    uninstaller_root_window.mainloop()

if "--uninstall" in sys.argv:
    # Run the uninstaller if it this executable is called in that way.
    uninstaller()
elif "--uac" in sys.argv:
    # If the app is restarted 
    installer(True)
else:
    installer(False)

