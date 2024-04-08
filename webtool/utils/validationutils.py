#
# This file is to validate different user values of the web tool. All validation should originate from
#   here unless it is a simple empty check
#

import re


# method to validate tkinter entry for an integer
def validate_int(result_value, callback_reason=None, min_value=None, max_value=None, character_limit=None):
    number_regex = "^[-]?[0-9]+$"

    if callback_reason is None:
        if re.match(number_regex, result_value):
            if max_value is not None and int(result_value) > int(max_value):
                return False
            if min_value is not None and int(result_value) < int(min_value):
                return False
            if character_limit is not None and len(result_value) > int(character_limit):
                return False
        else:
            return False

    if callback_reason is not None:
        if len(result_value) == 0:
            return True
        elif result_value == '-':
            if max_value is not None and int(max_value) < 0:
                return False
            if min_value is not None and int(min_value) >= 0:
                return False
        elif character_limit is not None and len(result_value) > int(character_limit):
            return False
        elif re.match(number_regex, result_value):
            if max_value is not None:
                if int(result_value) > int(max_value):
                    return False
            if min_value is not None:
                if int(result_value) < int(min_value) and callback_reason != 'key':
                    return False
    return True

# method to validate strings for tkinter entry, checking for character limits and characters allowed.
def validate_string(result_value, callback_reason=None, allowed_chars=None, character_min=None, character_max=None):
    return False
