from src.config.logging_config import get_logger


logger = get_logger("logging_test")


logger.info("Pipeline started successfully.")

logger.warning("This is a warning message.")

logger.error("This is an error message.")

logger.critical("This is a critical message.")