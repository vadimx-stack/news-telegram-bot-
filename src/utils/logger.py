import os
import sys
from loguru import logger


def setup_logger() -> None:
    """Настройка логгера для приложения."""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    
    logger.remove()
    logger.add(
        sys.stderr,
        level=log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    logger.add(
        "logs/newspulsebot.log",
        rotation="10 MB",
        retention="1 week",
        level=log_level,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    )

    logger.info("Логгер настроен с уровнем: {}", log_level) 