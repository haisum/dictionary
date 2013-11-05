"""
Setting up the logging handlers
see http://docs.python.org/dev/library/logging.handlers.html#logging.handlers.RotatingFileHandler for details
on what handlers are available SMTPHandler seems intersting and will implement it once we are in production

RotatingFileHandler logs everything to application.log untill we reach 2MB then it creates backup with name
application.log.1, application.log.2 till application.log.5 cycle continues by renaming the oldest backup file
logs are always written to application.log
"""
from core import app
# if not app.debug:
import os
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

file_handler = RotatingFileHandler(os.path.dirname(os.path.realpath(__file__))+"/../logs/application.log", mode="a", maxBytes=2*1024*1024, backupCount=5)

"""could be logging.ERROR or logging.DEBUG"""
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))

app.logger.addHandler(file_handler)

