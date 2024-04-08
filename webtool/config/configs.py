#
# This file is for a number of configurations that will be applied to the application
#

LOG_ENV = "dev"     # determines the logging schema to use and allows all modules to get the same logger

INSTALLATION_LOCATION = "_MEIPASS"  # a sys attribute created by pyinstaller when bundled

LOG_FILE_LOCATION = "logs"
LOG_FILE = "log.log"

# logging dictionary schema
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s [%(levelname)s] %(filename)s: %(message)s'
        },
        'extended': {
            'format': '%(asctime)s - %(levelname)s - %(name)s - %(filename)s:%(lineno)d - %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'formatter': 'simple',
            'filename': '',         # handled in the logging utils
            'class': 'logging.FileHandler',
        },
        'file_dev': {
            'level': 'DEBUG',
            'formatter': 'extended',
            'filename': '',         # handled in the logging utils
            'class': 'logging.FileHandler',
        },
        'console': {
            'level': 'INFO',
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'console_dev': {
            'level': 'DEBUG',
            'formatter': 'extended',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    },
    'loggers': {
        '': {       # root logger; used for production settings
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        },
        'test': {   # logger used for testing general functionality
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': False
        },
        'dev': {    # logger used for debugging issues and indepth analysis
            'handlers': ['file_dev', 'console_dev'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}
