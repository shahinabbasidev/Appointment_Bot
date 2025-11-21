import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
bot_db = os.getenv("BOT_DB")


def connect_db():
    conn = sqlite3.connect(bot_db)
    cursor = conn.cursor()
    return conn, cursor

#insert user
def insert_db(user_id,user_name):
    conn, cursor = connect_db()
    cursor.execute('''INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?, ?)''' , (user_id,user_name))

    conn.commit()
    conn.close()

# select
def show_available_services():
    conn, cursor = connect_db()
    cursor.execute('SELECT service_id, name FROM services')
    services = cursor.fetchall()

    conn.close()
    return services


def get_date(service_id):
    conn, cursor = connect_db()
    cursor.execute('SELECT DISTINCT date FROM slots WHERE service_id = ?', (service_id,))
    date = [row[0] for row in cursor.fetchall()]
    conn.close()
    return date


def get_time(service_id, date):
    conn, cursor = connect_db()
    cursor.execute(
        '''
        SELECT slot_id, time FROM slots
        WHERE service_id = ? AND slot_date = (?) AND slot_status = 'available'
        ORDER BY slot_time ASC
        ''',(service_id, date)
    )
    times = cursor.fetchall()
    conn.close()
    return times


















