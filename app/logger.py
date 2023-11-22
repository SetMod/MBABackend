import logging
import os
import sys

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

base_format = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)s] [%(filename)s:%(funcName)s:%(lineno)d]: %(message)s"
)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(base_format)
stream_handler.setLevel(logging.INFO)
logger.addHandler(stream_handler)

filepath = os.path.dirname(os.path.dirname(__file__))
filepath = os.path.join(filepath, "tmp.log")
file_handler = logging.FileHandler(filename=filepath, mode="w", encoding="utf8")
file_handler.setFormatter(base_format)
file_handler.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
