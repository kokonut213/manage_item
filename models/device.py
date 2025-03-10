import sqlite3
from flask import g  # Import đối tượng g từ flask

DATABASE_NAME = 'manageitem_db.db' # Cập nhật tên database

class DeviceModel:
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

    def add_device(self, device_name, device_type, brand, location, status):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO devices (device_name, device_type, brand, location, status)
            VALUES (?, ?, ?, ?, ? )
        """, (device_name, device_type, brand, location, status))
        conn.commit()

    def get_device_by_id(self, device_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        device = cursor.execute("""
            SELECT * FROM devices WHERE id = ?
        """, (device_id,)).fetchone()
        return device

    def get_all_devices(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        devices = cursor.execute("""
            SELECT * FROM devices
        """).fetchall()
        return devices

    def update_device(self, device_id, device_name, device_type, brand, location, status):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE devices SET device_name = ?, device_type = ?, brand = ?, location = ?, status = ?
            WHERE id = ?
        """, (device_name, device_type, brand, location, status, device_id))
        conn.commit()

    def delete_device(self, device_id):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM devices WHERE id = ?
        """, (device_id,))
        conn.commit()

    def search_devices(self, keyword):
        conn = self.get_db_connection()
        keyword = '%' + keyword + '%'
        cursor = conn.cursor()
        devices = cursor.execute("""
            SELECT * FROM devices
            WHERE device_name LIKE ? OR device_type LIKE ? OR brand LIKE ? OR location LIKE ? OR status LIKE ?
        """, (keyword, keyword, keyword, keyword, keyword)).fetchall()
        return devices
    def get_devices_by_statuses(self, statuses):
        """Lấy danh sách thiết bị theo danh sách trạng thái."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        placeholders = ','.join('?' * len(statuses)) # Tạo placeholders cho IN clause
        devices = cursor.execute(f"""
            SELECT * FROM devices
            WHERE status IN ({placeholders})
        """, statuses).fetchall()
        return devices

    def update_device_status(self, device_id, status):
        """Cập nhật chỉ trạng thái thiết bị."""
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE devices SET status = ?
            WHERE id = ?
        """, (status, device_id))
        conn.commit()

    def search_devices_by_statuses(self, keyword, statuses):
        """Tìm kiếm thiết bị theo keyword và danh sách trạng thái."""
        conn = self.get_db_connection()
        keyword = '%' + keyword + '%'
        placeholders = ','.join('?' * len(statuses))
        cursor = conn.cursor()
        devices = cursor.execute(f"""
            SELECT * FROM devices
            WHERE (device_name LIKE ? OR device_type LIKE ? OR brand LIKE ? OR location LIKE ? OR status LIKE ?)
            AND status IN ({placeholders})
        """, (keyword, keyword, keyword, keyword, keyword, *statuses)).fetchall() # *statuses để unpack danh sách
        return devices