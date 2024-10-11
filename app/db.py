import sqlite3

from config import DATABASE_NAME

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Таблица для хранения показаний счетчиков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS meters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            water_meter REAL,
            electricity_meter REAL
        )
    ''')

    # Таблица для хранения текущих показаний счетчиков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS current_meters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            water_meter REAL,
            electricity_meter REAL
        )
    ''')

    # Таблица для хранения стоимости ресурсов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            water_cost REAL,
            electricity_cost REAL
        )
    ''')

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DATABASE_NAME)