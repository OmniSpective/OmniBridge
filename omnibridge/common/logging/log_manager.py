import logging
from datetime import datetime
from typing import Any

class LogManager:
    """
    LogManager is a centralized logging class that configures and manages logging for an application.
    It sets up a logger with both stream and file handlers, allowing log messages to be output to the console
    and a file simultaneously. LogManager uses a singleton pattern to ensure only one instance is created
    throughout the application.

    Attributes:
        FORMATTER (logging.Formatter): Formatter for the log messages.
        STREAM_LOG_LEVEL (int): The log level for the stream handler (default: logging.ERROR).
        FILE_LOG_LEVEL (int): The log level for the file handler (default: logging.DEBUG).
        LOG_FILE_NAME (str): The name of the log file with the current date.
        LOGGER_NAME (str): The name of the logger.

    Example:
        log_manager = LogManager()
        logger = log_manager.logger

        logger.debug("This is a debug message.")
        logger.info("This is an info message.")
        logger.warning("This is a warning message.")
        logger.error("This is an error message.")
        logger.critical("This is a critical message.")
    """
    _instance: Any = None
    _initialized: bool = False

    FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')
    STREAM_LOG_LEVEL = logging.ERROR
    FILE_LOG_LEVEL = logging.DEBUG
    LOG_FILE_NAME = ".log-" + datetime.today().strftime('%d-%m-%Y')
    LOGGER_NAME = "OmniSpectiveLogger"

    def __new__(cls: Any) -> Any:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, stream_log_level: int = STREAM_LOG_LEVEL) -> None:
        if self._initialized:
            return
        
        logger = logging.getLogger(LogManager.LOGGER_NAME)
        logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(stream_log_level)
        stream_handler.setFormatter(LogManager.FORMATTER)

        file_handler = logging.FileHandler(LogManager.LOG_FILE_NAME)
        file_handler.setLevel(LogManager.FILE_LOG_LEVEL)
        file_handler.setFormatter(LogManager.FORMATTER)

        logger.addHandler(stream_handler)
        logger.addHandler(file_handler)

        self._logger = logger

        self._initialized = True

    @property
    def logger(self) -> logging.Logger:
        return self._logger
