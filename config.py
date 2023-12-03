import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHANEL_ID = os.getenv('CHAT')
ADMIN_1 = os.getenv('ADMIN_1')
ADMIN_2 = os.getenv('ADMIN_2')

if TELEGRAM_TOKEN is None:
    raise Exception("Переменная <TELEGRAM_TOKEN> не установлена.")

if CHANEL_ID is None:
    raise Exception("Переменная <CHAT> не установлена.")

POSTGRES_USERNAME = os.getenv('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT: int = int(os.getenv('POSTGRES_PORT'))
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')

# Redis
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_USER = os.getenv('REDIS_USER')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
