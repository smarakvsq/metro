import logging
import logging.config
import os.path as op
import sys

from app.config import Settings
from app.constants import FilePath

settings = Settings()
# Configure logging using the configuration file
app_logger = logging.getLogger("webapp")
task_logger = logging.getLogger("background")

app_logger.propagate = False
task_logger.propagate = False

formatter = logging.Formatter(fmt="%(asctime)s | %(levelname)s | %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
app_file_handler = logging.FileHandler(op.join(FilePath.APP_LOG_PATH, "app.log"))
task_file_handler = logging.FileHandler(op.join(FilePath.TASK_LOG_PATH, "task.log"))

for hlr in [stream_handler, app_file_handler, task_file_handler]:
    hlr.setFormatter(formatter)

app_logger.handlers = [stream_handler, app_file_handler]
task_logger.handlers = [stream_handler, task_file_handler]

app_logger.setLevel(settings.log_level)
task_logger.setLevel(settings.log_level)
