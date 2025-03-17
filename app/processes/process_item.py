from app.configs.logger import logger


def process_item(item):
    logger.info(f'Processing {item['product']}')
