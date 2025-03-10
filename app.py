from flask import Flask, render_template, request, redirect, url_for, flash, session
from controllers.device_controller import DeviceController
from controllers.auth_controller import AuthController # Import AuthController
from models.device import DeviceModel

app = Flask(__name__)
app.secret_key = "your_secret_key"

device_controller = DeviceController()
auth_controller = AuthController() # Khởi tạo AuthController
device_model = DeviceModel()

# --- HÀM HỖ TRỢ PHÂN QUYỀN ---
def is_admin():
    return session.get('user_role') == 'admin'

def is_staff():
    return session.get('user_role') == 'staff'

def admin_login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash("Yêu cầu quyền admin để truy cập trang này.", "warning")
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

def staff_login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_staff() and not is_admin():
            flash("Yêu cầu quyền staff để truy cập trang này.", "warning")
            return redirect(url_for('staff_login'))
        return f(*args, **kwargs)
    return decorated_function

# --- ROUTES AUTHENTICATION ---
@app.route('/admin/register', methods=['GET', 'POST'])
def register_admin_route():
    if request.method == 'POST':
        return auth_controller.register_admin()
    return auth_controller.register_admin_form()

@app.route('/staff/register', methods=['GET', 'POST'])
def register_staff_route():
    if request.method == 'POST':
        return auth_controller.register_staff()
    return auth_controller.register_staff_form()

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    return auth_controller.login_admin() # Gọi method login từ AuthController

@app.route('/staff/login', methods=['GET', 'POST'])
def staff_login():
    return auth_controller.login_staff() # Gọi method login từ AuthController

@app.route('/admin/logout')
def admin_logout():
    return auth_controller.logout_admin() # Gọi method logout từ AuthController

@app.route('/staff/logout')
def staff_logout():
    return auth_controller.logout_staff() # Gọi method logout từ AuthController


# --- ROUTES ADMIN ---
@app.route('/admin/devices')
@admin_login_required
def admin_devices():
    return device_controller.list_devices()

@app.route('/admin/devices/add', methods=['GET', 'POST'])
@admin_login_required
def admin_add_device():
    if request.method == 'POST':
        return device_controller.create_device()
    return device_controller.add_device_form()

@app.route('/admin/devices/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_required
def admin_edit_device(id):
    if request.method == 'POST':
        return device_controller.update_device(id)
    return device_controller.edit_device_form(id)

@app.route('/admin/devices/delete/<int:id>')
@admin_login_required
def admin_delete_device(id):
    return device_controller.delete_device(id)

@app.route('/admin/devices/search', methods=['GET', 'POST'])
@admin_login_required
def admin_search_devices():
    return device_controller.search_devices()

# --- ROUTES STAFF ---
@app.route('/staff/devices')
@staff_login_required
def staff_devices():
    return device_controller.list_devices_staff()

@app.route('/staff/devices/edit_status/<int:id>', methods=['GET', 'POST'])
@staff_login_required
def staff_edit_device_status(id):
    if request.method == 'POST':
        return device_controller.update_device_status(id)
    return device_controller.edit_device_status_form(id)

@app.route('/staff/devices/search', methods=['GET', 'POST'])
@staff_login_required
def staff_search_devices():
    return device_controller.search_devices_staff()


# --- ROUTES CÔNG KHAI ---
@app.route('/')
def index():
    return device_controller.list_devices()

@app.route('/search', methods=['GET', 'POST'])
def search():
    return device_controller.search_devices()

@app.teardown_appcontext
def close_connection(exception):
    device_model.close_db_connection()

if __name__ == '__main__':
    app.run(debug=True)