#
# This is a web tool for searching and mapping websites. It cycles through any list of urls and looks for specified
#  strings within those urls as well as can map a website starting providing the link to the home screen.
#
# @author Dominic Dangerfield
# @contact dominic.t.dangerfield@gmail.com
#

from webtool.app.application import Application
from webtool.utils.loggingutils import setup_logging, get_logger


setup_logging()
logger = get_logger()
logger.debug("Logger is established")

if __name__ == '__main__':
    tkinter_window = Application()
    logger.debug("Application is running")
    tkinter_window.mainloop()
