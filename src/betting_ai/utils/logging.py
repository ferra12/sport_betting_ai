import logging
import sys


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._setup_logger()
        return cls._instance

    def _setup_logger(self):
        self.logger = logging.getLogger("nutri_app")
        self.logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="[%(filename)s:%(lineno)d] : %(asctime)s - %(levelname)s - %(message)s ",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        if not self.logger.hasHandlers():
            self.logger.addHandler(handler)

    def debug(self, msg):
        self.logger.debug(msg, stacklevel=2)

    def info(self, msg):
        self.logger.info(msg, stacklevel=2)

    def warning(self, msg):
        self.logger.warning(msg, stacklevel=2)

    def error(self, msg):
        self.logger.error(msg, stacklevel=2)


logger = Logger()

if __name__ == "__main__":
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")