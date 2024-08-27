import bcrypt
import sqlite3

def sign_up(username, password):
    password = password.encode('utf-8')
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (username, password) VALUES (?, ?)
        ''', (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def log_in(username, password):
    password = password.encode('utf-8')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT password FROM users WHERE username = ?
    ''', (username,))
    result = cursor.fetchone()

    conn.close()

    if result and bcrypt.checkpw(password, result[0]):
        return True
    else:
        return False

