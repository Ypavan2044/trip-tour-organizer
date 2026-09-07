import pymysql

from db import create_connection
from validation import get_valid_email


def register():
    print("\n========== REGISTER ==========")
    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    email = get_valid_email()
    password = input("Enter your password: ")
    if len(password) < 3:
        print("Password must contain at least 3 characters.")
        return
    conn = None
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, 'viewer')",
                (name, email, password)
            )
        conn.commit()
        print("Registration successful! ✅")
    except pymysql.err.IntegrityError:
        if conn:
            conn.rollback()
        print("Email already exists.")
    except pymysql.MySQLError as e:
        if conn:
            conn.rollback()
        print("Database error:", e)
    finally:
        if conn:
            conn.close()
def login():
    print("\n========== LOGIN ==========")
    email = input("Enter your email: ").strip()
    password = input("Enter your password: ")
    conn = None
    try:
        conn = create_connection()
        with conn.cursor() as cur:
            cur.execute(
                "SELECT user_id, name, password, role FROM users WHERE email=%s",
                (email,)
            )
            user = cur.fetchone()
            if user and password == user[2]:
                print(f"\nWelcome, {user[1]}! ")
                return user[0], user[3]
            else:
                print("Invalid email or password.")
    except pymysql.MySQLError as e:
        print("Database error:", e)
    finally:
        if conn:
            conn.close()
    return None, None