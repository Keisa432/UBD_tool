import logging
import os
import sys

abs_path = os.path.dirname(os.path.abspath(sys.argv[0]))
logging_path = os.path.join(abs_path, "ubd_log.txt")

if os.path.exists(logging_path):
    os.remove(logging_path)

logging.basicConfig(filename=logging_path,
                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(message)s')


def log_msg(name, level, message):
    logger = logging.getLogger(name)
    if level == 0:
        logger.info(message)
    elif level == 1:
        logger.warning(message)
    elif level == 2:
        logger.error(message)
    else:
        logger.debug(message)
