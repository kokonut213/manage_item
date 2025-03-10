from flask import render_template, request, redirect, url_for, flash, session
from models.device import DeviceModel
import os
from werkzeug.utils import secure_filename

class DeviceController:
   
    def __init__(self):
        self.model = DeviceModel()

   
    # --- METHODS ADMIN (đã có và chỉnh sửa) ---
    def list_devices(self): # Giữ nguyên, admin xem full list
        devices = self.model.get_all_devices()
        return render_template("list_devices.html", devices=devices)

    def add_device_form(self): # Giữ nguyên
        return render_template("add_edit_device.html", device=None, action='add')

    def edit_device_form(self, device_id): # Giữ nguyên
        device = self.model.get_device_by_id(device_id)
        if not device:
            return "Thiết bị không tồn tại", 404
        return render_template("add_edit_device.html", device=device, action='edit') # THÊM action='edit'

    def create_device(self):
   

     if request.method == 'POST':
        print("Method là POST")
        device_name = request.form['device_name']
        device_type = request.form['device_type']
        brand = request.form['brand']
        location = request.form['location']
        status = request.form['status']

        # Xóa phần code xử lý file ảnh (tải lên, lưu file, kiểm tra file...)
        # ...

        # Lưu thông tin thiết bị vào database (KHÔNG có đường dẫn ảnh)
        self.model.add_device(device_name, device_type, brand, location, status) # Loại bỏ device_image_path
        flash('Thêm thiết bị thành công!', 'success')
        return redirect(url_for('admin_devices'))
     else:
        print("Method KHÔNG phải POST")
        return redirect(url_for('admin_add_device'))
     
    def update_device(self, device_id):
     if request.method == 'POST':
        device_name = request.form['device_name']
        device_type = request.form['device_type']
        brand = request.form['brand']
        location = request.form['location']
        status = request.form['status']

        # Xóa phần code xử lý file ảnh (tải lên, lưu file, xóa ảnh cũ...)
        # ...

        self.model.update_device(device_id, device_name, device_type, brand, location, status) # Cập nhật KHÔNG có device_image_path
        flash('Cập nhật thiết bị thành công!', 'success')
        return redirect(url_for('admin_devices'))
     return redirect(url_for('admin_edit_device', id=device_id))

    def delete_device(self, device_id): # Giữ nguyên (có thể mở rộng để xóa ảnh sau)
        device = self.model.get_device_by_id(device_id) # Lấy thông tin thiết bị trước khi xóa
        image_path = device['device_image_path'] # Lấy đường dẫn ảnh

        self.model.delete_device(device_id) # Xóa thiết bị khỏi DB

        if image_path and os.path.exists(image_path): # Kiểm tra đường dẫn và file tồn tại
            try:
                os.remove(image_path) # Xóa file ảnh
                print(f"Đã xóa file ảnh: {image_path}")
            except Exception as e:
                print(f"Lỗi khi xóa file ảnh: {e}")

        return redirect(url_for('admin_devices')) # Redirect về admin_devices

    def search_devices(self): # Giữ nguyên, admin search full list
        if request.method == 'POST':
            keyword = request.form['keyword']
            devices = self.model.search_devices(keyword)
            return render_template('list_devices.html', devices=devices, search_keyword=keyword)
        return render_template('list_devices.html', devices=self.model.get_all_devices())

    # --- METHODS STAFF (thêm mới) ---
    def list_devices_staff(self):
        """Hiển thị danh sách thiết bị hỏng/cần sửa chữa cho staff."""
        statuses = ['Hỏng', 'Cần sửa chữa']
        devices = self.model.get_devices_by_statuses(statuses) # Tạo method get_devices_by_statuses trong model
        return render_template("staff/list_devices_staff.html", devices=devices) # Tạo template staff/list_devices_staff.html

    def edit_device_status_form(self, device_id):
        """Hiển thị form sửa tình trạng thiết bị cho staff."""
        device = self.model.get_device_by_id(device_id)
        if not device:
            return "Thiết bị không tồn tại", 404
        return render_template("staff/edit_device_status.html", device=device) # Tạo template staff/edit_device_status.html

    def update_device_status(self, device_id):
        """Xử lý cập nhật tình trạng thiết bị cho staff."""
        if request.method == 'POST':
            status = request.form['status']
            self.model.update_device_status(device_id, status) # Tạo method update_device_status trong model
            return redirect(url_for('staff_devices')) # Redirect về staff_devices

    def search_devices_staff(self):
        """Tìm kiếm trong danh sách thiết bị hỏng/cần sửa chữa cho staff."""
        if request.method == 'POST':
            keyword = request.form['keyword']
            statuses = ['Hỏng', 'Cần sửa chữa'] # Tìm kiếm trong danh sách thiết bị hỏng/cần sửa chữa
            devices = self.model.search_devices_by_statuses(keyword, statuses) # Tạo method search_devices_by_statuses
            return render_template('staff/list_devices_staff.html', devices=devices, search_keyword=keyword)
        statuses = ['Hỏng', 'Cần sửa chữa']
        devices = self.model.get_devices_by_statuses(statuses)
        return render_template('staff/list_devices_staff.html', devices=devices)