import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(r"logs/app.log", encoding="utf-8")
stream_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

