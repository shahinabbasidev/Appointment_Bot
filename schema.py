import sqlite3


conn = sqlite3.connect('appointment_service.db')
cursor = conn.cursor()

#User Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS users (
        user_id TEXT PRIMARY KEY,
        user_name TEXT
    )
    '''
)

# Service Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS services (
    service_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    admin_id TEXT
    )
    '''
)

# Slot Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS slots (
    slot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    time TEXT,
    status INTEGER DEFAULT 'available',
    service_id INTEGER
    )
    '''
)
#Appointment Table
cursor.execute(
    '''
    CREATE TABLE IF NOT EXISTS appointments (
    app_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT,
    slot_id INTEGER
    )
    '''
)




conn.commit()
conn.close()