import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

stream_logger = logging.StreamHandler()
stream_logger.setLevel(logging.INFO)

logger.addHandler(stream_logger)
