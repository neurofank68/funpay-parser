import logging

logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
