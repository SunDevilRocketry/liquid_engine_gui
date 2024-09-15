# Rocket Engine GUI
This branch has the goal of creating an easy executable installer for the liquid_engine_gui.

## TODO

- [ ]  Change directory structure to conventional Python3 module
- [ ]  Create pysetup.toml
- [ ]  Remove sdec submodule and update documentation saying that sdec is installed with pip.
- [ ]  Setup packaging (perhaps through something as simple as pyinstall to make one EXE, but it could also be an installer that 1. sets up a Python environment, 2. installs SDR software, 3. Installs a .BAT that executes our applications with the installed Python)

## Getting Started
1) Open cmd / terminal
2) Navigate into the project folder
3) Ensure all required libraries are downloaded (pip install -r requirements.txt)
4) Run main program (python SDR_LiquidGUI.py)
5) Connect Arduino running SDR_DataLogger_Analog.ino via USB port

The following code on this repository has been designed to control the SDR Liquid Engine Switchbox to:
- Automate Rocket Engine Startup
- Display Rocket Engine State
- Log Sensor Data
- Have Pre-programmed actions to execute (i.e. Startup)

## GUI Layout
<img src="images/engine_gui_2023.png">

