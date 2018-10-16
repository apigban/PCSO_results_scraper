import logging
import re
import sys
from datetime import datetime as dt
from inspect import currentframe
from logging.handlers import TimedRotatingFileHandler

frame = currentframe().f_back
while frame.f_code.co_filename.startswith('<frozen'):
    frame = frame.f_back

caller_name_string = frame.f_code.co_filename
pattern = r'(?:.*)/(.*)(?:\.py)'

caller_name = re.match(pattern, caller_name_string)

FORMATTER = logging.Formatter('%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s')
LOG_FILE = f'log/{caller_name.group(1)}_{dt.now().date()}.log'


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler():
    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler())
    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger
