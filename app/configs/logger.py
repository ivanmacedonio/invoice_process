import logging

logging.basicConfig(format='%(levelname)s ~ %(asctime)s - %(filename)s: %(message)s.',
                    datefmt='%d-%m-%Y %I:%M:%S', level=logging.DEBUG)

logger = logging.getLogger(__name__)
