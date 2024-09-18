import sys

from tkinter import *
from tkinter import ttk

# Standardized window creator, just to make sure window geometry is consistent between both version
def create_root_window():
    root_window = Tk()
    root_window.geometry("400x300")

    return root_window

# Function for running the Windows installation
def installer(admin_access):
    installer_root_window = create_root_window()

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

