import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
ADMINCHAT = os.getenv('CHAT')
ADMIN_1 = os.getenv('ADMIN_1')
ADMIN_2 = os.getenv('ADMIN_2')

if TELEGRAM_TOKEN is None:
    raise Exception("Переменная <TELEGRAM_TOKEN> не установлена.")

if ADMINCHAT is None:
    raise Exception("Переменная <CHAT> не установлена.")



