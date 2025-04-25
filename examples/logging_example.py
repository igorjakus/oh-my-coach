from loguru import logger

# Loguru configuration - file logging with rotation
logger.add(
    "logs/file_{time}.log",
    rotation="500 MB",  # New file after exceeding 500MB
    retention="10 days",  # Keep logs for 10 days
    compression="zip",  # Compress old logs
    level="INFO",
)


# Example of using different logging levels
def process_data(data):
    logger.debug(f"Starting data processing: {data}")
    try:
        # Error simulation
        result = 1 / 0
    except Exception:
        # Automatic full traceback logging
        logger.exception("Error occurred during processing")
        raise

    logger.success("Data processed successfully!")  # Unique 'success' level
    return result


if __name__ == "__main__":
    # Colored logging in terminal
    logger.info("Application starting...")
    logger.warning("This is a warning")

    try:
        process_data({"key": "value"})
    except Exception:
        logger.error("Failed to process data")
