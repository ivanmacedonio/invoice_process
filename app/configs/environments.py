import os
from dotenv import load_dotenv

load_dotenv()

# concurrency
WORKERS_AMOUNT = os.getenv('WORKERS_AMOUNT')

# payclub config
PVS_BASE_URL_PATH = os.getenv('PVS_BASE_URL_PATH')
PVS_CLIENT_ID = os.getenv('PVS_CLIENT_ID')
PVS_CLIENT_SECRET = os.getenv('PVS_CLIENT_SECRET')
PVS_APP_NAME = os.getenv('PVS_APP_NAME')
