#
# This file is do any web requests, given any set of arguments.
#   All requests should come from here
#

import re

import requests
from urllib.parse import urlparse, urljoin

from webtool.constants.constants import *
from webtool.utils.loggingutils import get_logger


# get the html of a webpage given some url and a session, allowing for timeout and retrying
def return_webpage(session, url, retry_quantity, timeout_limit):
    logger = get_logger()
    for i in range(retry_quantity):
        try:
            current_page = session.get(url, timeout=timeout_limit)
            return current_page
        except requests.exceptions.Timeout as timeoutError:
            # retry after connection/read timeout
            if i < retry_quantity - 1:
                continue
            else:
                logger.debug("URL {url} timed out".format(url=url))
                raise timeoutError


# get a standardized version of the url
def update_url(url, base_url=None, add_end_slash=False):
    logger = get_logger()
    # join the url with the base url for an absolute path
    if base_url is not None:
        standard_url = urljoin(base_url, url)
    else:
        standard_url = url

    # add '/' to the end of the url if appropriate
    #   (i.e. 'www.home.edu/directory', 'www.home.edu/directory/')
    if add_end_slash:
        parsed_url = urlparse(standard_url)
        # if this isn't a file, add a slash at the end of the
        if not re.search(has_any_file_ext_regex, parsed_url.path) or parsed_url.path == '':
            standard_url = urljoin(parsed_url.geturl(), "./")

    logger.debug("Standardized {old} to {new}".format(old=url, new=standard_url))

    return standard_url
