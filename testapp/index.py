from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import login_user, login_required

from testapp import dao, app
from testapp.dao import create_nextcloud_user
from testapp.models import *

# Route để trả về giao diện đăng ký người dùng
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Route để trả về giao diện đăng ký người dùng
@app.route('/register', methods=['GET'])
def show_register_page():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def view_login():
    err_msg = ''
    success_msg = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            err_msg = 'Username or password is missing'
            print(f"Login error: {err_msg}")  # In lỗi ra terminal
            return render_template('login.html', err_msg=err_msg)

        # In ra mật khẩu đã nhập
        print(f"Entered password: {password}")
        print(f"Entered username: {username}")

        # Kiểm tra người dùng trong cơ sở dữ liệu
        user = dao.auth_user(username=username, password=password)

        # In ra mật khẩu đã hash
        if user:
            print(f"Password from db: {user.password}")
            login_user(user=user)  # Đăng nhập người dùng vào session
            success_msg = 'Login successful!'
            print(f"Login success: {username} logged in successfully.")  # In thông báo thành công ra terminal
            # Sau khi đăng nhập thành công, chuyển hướng đến trang index
            return redirect(url_for('index'))
        else:
            err_msg = 'Invalid username or password'
            print(f"Login error: {err_msg}")  # In lỗi ra terminal
    return render_template('login.html', err_msg=err_msg)

# API đăng ký người dùng
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    quota = data.get('quota', 1024)

    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), 400

    # 1. Check nếu đã có user trong MySQL
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'Username or email already exists'}), 409

    # 3. Tạo user trên Nextcloud
    created = create_nextcloud_user(username, password, email)
    if not created:
        return jsonify({'error': 'Failed to create user on Nextcloud'}), 500

    # 4. Tạo user trong MySQL, lưu mật khẩu gốc mà không hash
    try:
        user = User(
            username=username,
            email=email,
            password=password,  # Lưu mật khẩu gốc vào CSDL
            quota=quota
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()  # Rollback nếu có lỗi
        return jsonify({'error': f'Error saving user to database: {str(e)}'}), 500

    return jsonify({'message': 'User created successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
