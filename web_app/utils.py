import os
import logging
from datetime import datetime

def init_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def make_output_path(base, username):
    folder = os.path.join(base, username)
    os.makedirs(folder, exist_ok=True)
    return folder

def make_filename(username, timestamp: datetime, ext, shortcode=None):
    clean_time = timestamp.strftime("%Y%m%dT%H%M%S")
    if shortcode:
        return f"{username}_{clean_time}_{shortcode}.{ext}"
    return f"{username}_{clean_time}.{ext}"

LOG = logging.getLogger("StoryScraper")
