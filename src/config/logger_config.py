import asyncio
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class CoroutineFormatter(logging.Formatter):
    def format(self, record):
        try:
            current_task = asyncio.current_task()
            record.coroutine_name = current_task.get_name() if current_task else "NoTask"
        except RuntimeError:
            record.coroutine_name = "NoLoop"
        return super().format(record)

    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
            return s[:-3]
        else:
            t = dt.strftime('%Y-%m-%d %H:%M:%S')
            return f"{t}.{int(record.msecs):03d}"


def configure_logging(log_dir: str):
    start_time = datetime.now().strftime("%d_%m_%Y__%H_%M_%S")
    log_file_path = os.path.join(log_dir, f'log_{start_time}.txt')

    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=5 * 1024 * 1024,
        backupCount=10,
    )

    console_handler = logging.StreamHandler()

    formatter = CoroutineFormatter(
        '%(asctime)s [%(coroutine_name)s] %(levelname)s %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S.%f',
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler],
    )

    logging.getLogger('apscheduler').setLevel(logging.WARNING)