import sqlite3
from werkzeug.security import generate_password_hash # Import để hash password

DATABASE_NAME = 'manageitem_db.db'

def create_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Bảng devices (đã có)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS devices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_name TEXT,
            device_type TEXT,
            brand TEXT,
            location TEXT,
            status TEXT
        )
    """)

    # Bảng users (thêm mới)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL  -- 'admin' hoặc 'staff'
        )
    """)

    conn.commit()
    conn.close()

def create_default_users(): # Hàm tạo user admin và staff mặc định (ví dụ)
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Kiểm tra xem user admin đã tồn tại chưa
    cursor.execute("SELECT id FROM users WHERE username = ?", ('admin',))
    admin_exists = cursor.fetchone()
    if not admin_exists:
        admin_password_hash = generate_password_hash('password') # Hash password 'password'
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                       ('admin', admin_password_hash, 'admin'))

    # Kiểm tra xem user staff đã tồn tại chưa
    cursor.execute("SELECT id FROM users WHERE username = ?", ('staff',))
    staff_exists = cursor.fetchone()
    if not staff_exists:
        staff_password_hash = generate_password_hash('password') # Hash password 'password'
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                       ('staff', staff_password_hash, 'staff'))

    conn.commit()
    conn.close()
    print("Đã tạo user admin và staff mặc định (nếu chưa tồn tại) - mật khẩu là 'password'")


if __name__ == '__main__':
    create_table()
    print(f"Bảng 'devices' và 'users' đã được tạo (nếu chưa tồn tại) trong '{DATABASE_NAME}'")
    create_default_users() # Gọi hàm tạo user mặc định