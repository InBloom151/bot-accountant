import sqlite3

from config import DATABASE_NAME

def init_db():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Таблица для хранения показаний счетчиков
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS units (
            water_unit REAL,
            electricity_unit REAL
        )
    ''')

    # Таблица для хранения стоимости ресурсов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS costs (
            water_cost REAL,
            electricity_cost REAL
        )
    ''')

    # Таблица для хранения итоговой стоимости
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS total_cost (
            total_cost REAL
        )
    ''')

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DATABASE_NAME)