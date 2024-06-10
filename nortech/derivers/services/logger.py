import os
from logging import basicConfig, getLogger

basicConfig(level=os.environ.get("LOG_LEVEL", "DEBUG"))
logger = getLogger()
