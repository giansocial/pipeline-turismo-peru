import logging
import sys
from src.config.settings import LOG_DIR, LOG_LEVEL


def setup_logging() -> None:
    fmt = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
    handlers = [
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "pipeline.log", encoding="utf-8"),
    ]
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format=fmt,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=handlers,
    )
