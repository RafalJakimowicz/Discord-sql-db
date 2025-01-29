from .database import *
import logging

__all__ = ['Database']

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Get the root logger
logger = logging.getLogger(__name__)