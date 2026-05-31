import logging
import sys
from pathlib import Path
from loguru import logger

# Create logs directory if it does not exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

class InterceptHandler(logging.Handler):
    """
    Default handler to intercept standard logging calls and route them through Loguru.
    """
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where the logged message originated
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

def setup_logger():
    """
    Configures and overrides standard library logging handlers to use Loguru.
    """
    # Remove existing handlers for both root logger and uvicorn loggers
    logging.root.handlers = []
    for logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error", "fastapi"):
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = []
        logging_logger.propagate = False

    # Intercept everything
    logging.basicConfig(handlers=[InterceptHandler()], level=0)

    # Configure Loguru
    config = {
        "handlers": [
            {
                "sink": sys.stdout,
                "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
                "level": "INFO",
            },
            {
                "sink": str(LOG_FILE),
                "format": "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message}",
                "level": "DEBUG",
                "rotation": "500 MB",
                "retention": "10 days",
                "compression": "zip",
            }
        ]
    }
    
    logger.configure(**config)
    logger.info("Structured logging has been fully initialized.")

# Run initial setup immediately upon import
setup_logger()
