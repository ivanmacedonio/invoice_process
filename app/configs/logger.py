import logging
import logging.handlers
import queue
import threading

log_queue = queue.Queue()

queue_handler = logging.handlers.QueueHandler(log_queue)

logger = logging.getLogger("AppLogger")
logger.setLevel(logging.DEBUG)
logger.addHandler(queue_handler)

log_formatter = logging.Formatter(
    '%(levelname)s ~ %(asctime)s - %(message)s.', datefmt='%d-%m-%Y %I:%M:%S')


def log_listener():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)

    while True:
        record = log_queue.get()
        if record is None:
            break
        console_handler.handle(record)


listener_thread = threading.Thread(target=log_listener, daemon=True)
listener_thread.start()
