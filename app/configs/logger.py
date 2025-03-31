import logging
import logging.handlers
import queue
import threading
from app.configs.environments import WORKERS_AMOUNT

log_queue = queue.Queue()

queue_handler = logging.handlers.QueueHandler(log_queue)

def log_worker():
    while True:
        record = log_queue.get()
        if record is None:
            break
        logger = logging.getLogger(record.name)
        logger.handle(record)


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(message)s")
logger = logging.getLogger("Main")


def thread_task(thread_id):
    thread_name = f"Thread-{thread_id}"
    record = logging.LogRecord(
        thread_name, logging.INFO, "", 0, f"{thread_name} is working", None, None)
    log_queue.put(record)


log_thread = threading.Thread(target=log_worker, daemon=True)
log_thread.start()

threads = []
for i in range(int(WORKERS_AMOUNT)):
    thread = threading.Thread(target=thread_task, args=(i,))
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

log_queue.put(None)
log_thread.join()
