import sqlite3
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_NAME = 'manageitem_db.db'

class UserModel:
    def get_db_connection(self):
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = sqlite3.connect(DATABASE_NAME)
            db.row_factory = sqlite3.Row
        return db

    def close_db_connection(self):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()
            g._database = None

    def add_user(self, username, password, role):
        """Thêm user mới vào database."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        password_hash = generate_password_hash(password) # Hash mật khẩu trước khi lưu
        try:
            cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                           (username, password_hash, role))
            conn.commit()
            return True # Đăng ký thành công
        except sqlite3.IntegrityError: # Username đã tồn tại (UNIQUE constraint)
            return False # Đăng ký thất bại (username trùng)

    def get_user_by_username(self, username):
        """Lấy thông tin user theo username."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        user = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        return user

    def check_password(self, password_hash, password):
        """Kiểm tra mật khẩu đã nhập có khớp với hash trong database không."""
        return check_password_hash(password_hash, password)