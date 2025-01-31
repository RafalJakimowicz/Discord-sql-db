from .database import *
from .botendpoint import *
from .backendendpoint import *
import logging

__all__ = ['Database', 'BotEndpoint', 'BackendEndpoint']

logging.basicConfig(
    filename="logs.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Get the root logger
logger = logging.getLogger(__name__)