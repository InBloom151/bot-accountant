import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
ALLOWED_USERS = [int(i) for i in os.getenv('IDS').split(",")]
DATABASE_NAME = 'database.accountant_db'

buttons = [
    "1. Ввести показания счетчиков",
    "2. Ввести стоимость ресурсов",
    "3. Обновить показания счетчиков",
    "4. Обновить стоимость ресурсов",
    "5. Рассчитать стоимость"
]