#
# This is for all logging utilities
#

import logging.config
from os import makedirs, remove
from os.path import join, exists, isfile
from pathlib import Path

from webtool.config.configs import LOG_ENV, LOG_FILE_LOCATION, LOG_FILE, LOGGING_CONFIG
from webtool.utils.fileutils import open_dir, get_base_path


# get the logger
def get_logger():
    return logging.getLogger(LOG_ENV)


# Set up the configurations for logging and create the directory if needed
def setup_logging():
    base_path = get_base_path()

    log_folder_path = join(base_path, LOG_FILE_LOCATION)
    log_file_path = join(base_path, LOG_FILE_LOCATION, LOG_FILE)

    # create the folder if it doesn't exist
    if not exists(log_folder_path):
        makedirs(log_folder_path)

    # create the log file
    if not exists(log_file_path):
        open(log_file_path, "w").close()

    # have to do this here; cannot be blank and has to be a valid file location
    LOGGING_CONFIG["handlers"]["file"].update({"filename": log_file_path})
    LOGGING_CONFIG["handlers"]["file_dev"].update({"filename": log_file_path})

    logging.config.dictConfig(LOGGING_CONFIG)


# Get the location of the logging file to refer to if there are any issues
def get_logging_location():
    base_path = get_base_path()

    if not exists(join(base_path, LOG_FILE_LOCATION)):
        return "Log folder doesn't exist where expected"
    elif not isfile(join(base_path, LOG_FILE_LOCATION, LOG_FILE)):
        return "Log file doesn't exist where expected"
    else:
        return join(base_path, LOG_FILE_LOCATION, LOG_FILE)


# Open the folder of the log file; only accounting Windows and macOS for now.
def open_log_folder():
    directory = Path(str(get_logging_location())).parent
    open_dir(directory)


# Clear the log file's data
def clear_log():
    open(get_logging_location(), 'w').close()


# Delete the log file and folder from the user's system
def delete_log():
    remove(get_logging_location())
