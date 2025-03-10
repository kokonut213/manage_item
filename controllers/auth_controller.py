from flask import render_template, request, redirect, url_for, flash, session
from models.user import UserModel

class AuthController:
    def __init__(self):
        self.user_model = UserModel()

    def register_admin_form(self):
        """Hiển thị form đăng ký admin."""
        return render_template('admin/register.html')

    def register_staff_form(self):
        """Hiển thị form đăng ký staff."""
        return render_template('staff/register.html')

    def register_admin(self):
        """Xử lý đăng ký admin."""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if self.user_model.add_user(username, password, 'admin'):
                flash("Đăng ký admin thành công! Vui lòng đăng nhập.", "success")
                return redirect(url_for('admin_login'))
            else:
                flash("Đăng ký admin thất bại. Tên đăng nhập đã tồn tại.", "danger")
                return render_template('admin/register.html')

    def register_staff(self):
        """Xử lý đăng ký staff."""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            if self.user_model.add_user(username, password, 'staff'):
                flash("Đăng ký staff thành công! Vui lòng đăng nhập.", "success")
                return redirect(url_for('staff_login'))
            else:
                flash("Đăng ký staff thất bại. Tên đăng nhập đã tồn tại.", "danger")
                return render_template('staff/register.html')

    def login_admin(self):
        """Xử lý đăng nhập admin."""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = self.user_model.get_user_by_username(username)
            if user and self.user_model.check_password(user['password_hash'], password):
                session['user_role'] = user['role']
                flash("Đăng nhập admin thành công!", "success")
                return redirect(url_for('admin_devices'))
            else:
                flash("Đăng nhập admin thất bại. Sai tên đăng nhập hoặc mật khẩu.", "danger")
                return render_template('admin/login.html')
        return render_template('admin/login.html')

    def login_staff(self):
        """Xử lý đăng nhập staff."""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            user = self.user_model.get_user_by_username(username)
            if user and self.user_model.check_password(user['password_hash'], password):
                session['user_role'] = user['role']
                flash("Đăng nhập staff thành công!", "success")
                return redirect(url_for('staff_devices'))
            else:
                flash("Đăng nhập staff thất bại. Sai tên đăng nhập hoặc mật khẩu.", "danger")
                return render_template('staff/login.html')
        return render_template('staff/login.html')

    def logout_admin(self):
        """Xử lý đăng xuất admin."""
        session.pop('user_role', None)
        flash("Đã đăng xuất admin.", "info")
        return redirect(url_for('index'))

    def logout_staff(self):
        """Xử lý đăng xuất staff."""
        session.pop('user_role', None)
        flash("Đã đăng xuất staff.", "info")
        return redirect(url_for('index'))