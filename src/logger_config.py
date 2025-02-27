import sys

from loguru import logger


logger.add(
    "src/logs/app.log",
    rotation="10 MB",
    retention="1 day",
    level="ERROR",
    format="{level} | {time:YYYY-MM-DD HH:mm:ss} | {module} | {message}",
    enqueue=True,
)

logger.add(
    sys.stdout,
    format="{level} | {module} | {message}",
    enqueue=True,
)
