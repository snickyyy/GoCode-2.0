import logging

from config.settings import settings


def configure_logs():
    logging.basicConfig(
        level=settings.LOGS_LEVEL,
        format='[%(asctime)s.%(msecs)03d] %(filename)s:%(lineno)d:%(funcName)s %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
