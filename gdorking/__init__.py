"""Init file for gdorking package."""

import logging
import os

DEBUG = os.environ.get("DEBUG", False)
LOG_LEVEL = logging.DEBUG if DEBUG else logging.INFO

if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(LOG_LEVEL)
else:
    logging.basicConfig(level=LOG_LEVEL)


def get_root() -> str:
    """Get the root directory of the package."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_data_path() -> str:
    """Get the path to the data directory."""
    return os.path.join(get_root(), "data")
