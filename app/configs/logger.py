import logging
import threading
import queue

log_queue = queue.Queue()


class LogHandler(logging.Handler):
    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)


logging.basicConfig(format='%(levelname)s ~ %(asctime)s - %(filename)s: %(message)s.',
                    datefmt='%d-%m-%Y %I:%M:%S', level=logging.DEBUG)

logger = logging.getLogger(__name__)
logger.handlers.clear()
log_queue_handler = LogHandler(log_queue)
logger.addHandler(log_queue_handler)


def log_listener():
    while True:
        record = log_queue.get()
        if record is None or log_queue.empty():
            break
        logging.getLogger().handle(record)


log_thread = threading.Thread(
    target=log_listener, daemon=True
)
log_thread.start()
