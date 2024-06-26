#
# Utility methods for getting system information
#

from platform import platform


# get the OS that this is being run on
def get_os():
    current_platform = platform()

    if "macOS" in current_platform:
        return "macOS"
    elif "Windows" in current_platform:
        return "Windows"
    else:
        return None
