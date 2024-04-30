#
# Here is a list of all constants used throughout the project. Some item will be move
# int a configuration file as it is built
#

# Web Constants
url_protocol_options = ["http://", "https://", "file://"]
default_num_of_retries = 3
default_time_before_timeout = 3
has_any_file_ext_regex = "^((?![.]([a-z]*)))*$"
ignored_files_regex = "^((?![.]({ext})).)*$"

# Widget Constants
collapsible_texts = ["Collapse {object} <<", "Expand {object} >>"]

# File Constants
mapper_default_filename = "exported_mapper"

default_history_filename = "exported_history"
default_results_filename = "exported_results"
default_search_filename = "/search_file.xlsx"

all_files_ext = [("All Files", "*.*")]
excel_ext = [("Excel Files", "*.xlsx .xls")]
text_ext = [("Text Files", "*.txt")]
