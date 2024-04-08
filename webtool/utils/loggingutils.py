#
# This is for all logging utilities
#

import sys
import os.path
import pathlib
import platform

import logging.config

from webtool.config.configs import *


# get the logger
def get_logger():
    return logging.getLogger(LOG_ENV)


# Set up the configurations for logging and create the directory if needed
def setup_logging():
    if getattr(sys, 'frozen', False) and hasattr(sys, INSTALLATION_LOCATION):
        # system is running from an application
        base_path = str(pathlib.Path(getattr(sys, INSTALLATION_LOCATION)).absolute())
    else:
        # system is running from source
        base_path = str(pathlib.Path(os.getcwd()).absolute())

    log_folder_path = os.path.join(base_path, LOG_FILE_LOCATION)
    log_file_path = os.path.join(base_path, LOG_FILE_LOCATION, LOG_FILE)

    # create the folder if it doesn't exist
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)

    # create the log file
    if not os.path.exists(log_file_path):
        open(log_file_path, "w").close()

    # have to do this here; cannot be blank and has to be a valid file location
    LOGGING_CONFIG["handlers"]["file"].update({"filename": log_file_path})
    LOGGING_CONFIG["handlers"]["file_dev"].update({"filename": log_file_path})

    logging.config.dictConfig(LOGGING_CONFIG)


# Get the location of the logging file to refer to if there are any issues
def get_logging_location():
    if getattr(sys, 'frozen', False) and hasattr(sys, INSTALLATION_LOCATION):
        # system is running from an application
        base_path = getattr(sys, INSTALLATION_LOCATION)
    else:
        # system is running from source
        base_path = str(pathlib.Path(os.getcwd()).absolute())

    if not os.path.exists(os.path.join(base_path, LOG_FILE_LOCATION)):
        return "Log folder doesn't exist where expected"
    elif not os.path.isfile(os.path.join(base_path, LOG_FILE_LOCATION, LOG_FILE)):
        return "Log file doesn't exist where expected"
    else:
        return os.path.join(base_path, LOG_FILE_LOCATION, LOG_FILE)


# Open the folder of the log file; only accounting Windows, macOS, and Linx, mobile OS and such are not.
def open_log_folder():
    user_platform = platform.platform()
    match user_platform.split():
        case (*_, "macOS"):
            return "macOS"
        case (*_, "Windows"):
            return "Windows"
        case (*_, "Linux"):
            return "Linux"
        case _:
            return "Unrecognized"


# Clear the log file's data
def clear_log():
    return False


# Delete the log file and folder from the user's system
def delete_log():
    return False
