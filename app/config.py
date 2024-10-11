import os

from aiogram import types
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
ALLOWED_USERS = [int(i) for i in os.getenv('IDS').split(",")]
DATABASE_NAME = 'database.accountant_db'

buttons = [
    [types.KeyboardButton(text="1. Ввести показания счетчиков")],
    [types.KeyboardButton(text="2. Ввести стоимость ресурсов")],
    [types.KeyboardButton(text="3. Обновить показания счетчиков")],
    [types.KeyboardButton(text="4. Обновить стоимость ресурсов")],
    [types.KeyboardButton(text="5. Рассчитать стоимость")]
]