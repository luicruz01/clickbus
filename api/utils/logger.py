import os
import sys
import logging
import logging.handlers


def setup_logger(logger_name, level=logging.INFO, path='/var/log/ticketbus/'):
    watch_tower = os.environ.get('cloudwatch', '')

    if watch_tower in ('true', 'True'):
        handler = logging.FileHandler('/var/log/supervisor/api_server.log')
        handler.suffix = '%Y-%m-%d.log'
        logger = logging.getLogger(logger_name)
    else:
        handler = logging.handlers.TimedRotatingFileHandler(
            '%s%s.log' % (path, logger_name), 'midnight', 1, backupCount=2)
        handler.suffix = '%Y-%m-%d.log'
        logger = logging.getLogger(logger_name)

    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    logger.handlers = []
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)

    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            logger.info('Keyboard Interrupt')
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    # sys.excepthook = handle_exception
    return logger