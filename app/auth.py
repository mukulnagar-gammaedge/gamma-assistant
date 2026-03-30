import sqlite3
import hashlib
import uuid 
import sqlitecloud

#DB_PATH = "data/user.db"
DB_PATH = "sqlitecloud://cswafbzpdz.g6.sqlite.cloud:8860/auth.sqlitecloud?apikey=heGB8sIKfjZc0EbpLe8STKNPpA7VB4lkpAB9Z2xlWFo"

def init_db():
    conn = sqlitecloud.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id TEXT PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )

""")
    conn.commit()
    conn.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_user(username, password, role="user"):

    conn = sqlitecloud.connect(DB_PATH)

    cursor = conn.cursor()

    user_id = str(uuid.uuid4())

    hashed_pw = hash_password(password)

    cursor.execute("""

    INSERT INTO users (id, username, password, role)

    VALUES (?, ?, ?, ?)

    """, (user_id, username, hashed_pw, role))

    conn.commit()

    conn.close()

    return user_id



def authenticate_user(username, password):

    conn = sqlitecloud.connect(DB_PATH)

    cursor = conn.cursor()

    hashed_pw = hash_password(password)

    cursor.execute("""

    SELECT id, role FROM users

    WHERE username=? AND password=?

    """, (username, hashed_pw))

    result = cursor.fetchone()

    conn.close()

    return result


# simple token store (memory)
tokens = {}


def create_token(user_id, role):

    token = str(uuid.uuid4())

    tokens[token] = {

        "user_id": user_id,
        "role": role

    }

    return token


def verify_token(token):

    return tokens.get(token)


def delete_user(username):
    """Delete a user by username (useful for testing)"""
    try:
        conn = sqlitecloud.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return False


def get_user_by_username(username):
    """Get user by username (useful for testing)"""
    try:
        conn = sqlitecloud.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result
    except Exception:
        return None