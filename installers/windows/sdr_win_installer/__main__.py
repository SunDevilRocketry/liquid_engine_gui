#Standard Library imports
import sys
import os
import ctypes
from re import escape
from pathlib import Path
from zipfile import ZipFile

from tkinter import *
from tkinter import ttk

# Standardized window creator, just to make sure window geometry is consistent between both version
def create_root_window():
    root_window = Tk()
    root_window.geometry("400x300")

    return root_window

def installer_page_2(installer_root_window, install_type): # TODO add argument that tells this whether it'll be doing a user or a system install (or maybe just do it based on the --skip flag)
    # This page will do the actual install operations. For now,
    installing_frame = ttk.Frame(installer_root_window, padding=10)
    installing_frame.grid()

    installing_text = "Installing Sun Devil Rocketry Liquid Engine GUI and SDEC..."
    installing_label = ttk.Label(installing_frame, text=installing_text, wraplength=380)
    installing_label.grid(column=0, row=0)

    install_progress = IntVar()

    installing_progress_bar = ttk.Progressbar(installing_frame, length=380, variable=install_progress)
    installing_progress_bar.grid(column=0, row=1)

    install_progress.set(50)

    # Initialize variable for extraction path
    install_path = None

    if install_type == "system":
        install_path = "C:/Program Files/Sun Devil Rocketry"
    else:
        install_path = os.path.expandvars("$LOCALAPPDATA") + "/Sun Devil Rocketry"

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

    # Checks if the user is admin. If not, the application is restarted with UAC and flags passed into it.
    def check_admin():
        if not ctypes.windll.shell32.IsUserAnAdmin():
            # This checks if the command is actually running in the final executable or the development environment.
            # I had to do this crappy workaround because the field for executable flags for this function doesn't support escape sequences properly and my test Windows VM has a space in the username.
            if ".exe" in sys.argv[0]:
                # Final executable
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " --skip", os.getcwd(), 0)
            else:
                # Development environment
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " -m sdr_win_installer --skip", os.getcwd(), 0)
            
            installer_root_window.destroy()
        else:
            installer_page_2(installer_root_window, "system")

    def user_install():
        welcome_frame.destroy()
        installer_page_2(installer_root_window, "user")

    # System-wide Installation Button
    system_installation_button = ttk.Button(welcome_frame, text="System-Wide Installation", command=check_admin)
    system_installation_button.grid(column=0, row=1)

    # User installation Button
    user_installation_button = ttk.Button(welcome_frame, text="User Installation", command=user_install) # TODO Hook up to a function that opens page 2 to do a user install
    user_installation_button.grid(column = 0, row=2)

# Function for running the Windows installation
def installer(admin_access):
    print("Starting installation")
    installer_root_window = create_root_window()

    # Check if there is an existing installation of SDEC/Liquids GUI
    if not Path("C:/Program Files/Sun Devil Rocketry").exists() and not Path(os.path.expandvars("$LOCALAPPDATA") + "/Sun Devil Rocketry").exists() and not "--skip" in sys.argv:
        installer_page_1(installer_root_window)
    elif not Path("C:/Program Files/Sun Devil Rocketry").exists() and not Path(os.path.expandvars("$LOCALAPPDATA") + "/Sun Devil Rocketry").exists() and "--skip" in sys.argv:
        installer_page_2(installer_root_window, "system")
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

