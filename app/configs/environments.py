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

# database credentials
DATABASE_DRIVER = os.getenv('DATABASE_DRIVER')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# arca
ARCA_QR_CODE_GENERATOR_URL = os.getenv('ARCA_QR_CODE_GENERATOR_URL')

# mailchimp creds
MAILCHIMP_API_KEY = os.getenv('MAILCHIMP_API_KEY')
FROM_EMAIL = os.getenv('FROM_EMAIL')
