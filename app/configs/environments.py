import os
from dotenv import load_dotenv

load_dotenv()

WORKERS_AMOUNT = os.getenv('WORKERS_AMOUNT')
