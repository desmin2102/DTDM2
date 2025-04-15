import hashlib

import requests
from config import NEXTCLOUD_ADMIN_USERNAME, NEXTCLOUD_ADMIN_PASSWORD, NEXTCLOUD_URL
from testapp.models import User


# Tạo người dùng mới, gán dung lượng và thêm vào nhóm user mặc định
def create_nextcloud_user(username, password, email, quota_mb=1024):
    url = f"{NEXTCLOUD_URL}/ocs/v1.php/cloud/users"
    headers = {
        'OCS-APIRequest': 'true',
        'Content-Type': 'application/json',
    }

    data = {
        'userid': username,
        'password': password,
        'email': email,
    }

    try:
        print(f"Sending request to create user: {username}, email: {email}")
        response = requests.post(url, auth=(NEXTCLOUD_ADMIN_USERNAME, NEXTCLOUD_ADMIN_PASSWORD), headers=headers,
                                 json=data)

        # Log thêm chi tiết về response
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.text}")
        print(f"Response headers: {response.headers}")
        print(f"Response cookies: {response.cookies}")

        if response.status_code == 200:
            print(f"User {username} created successfully!")

            return True
        else:
            print(f"Error creating user {username}: {response.status_code}, {response.text}")
            return False
    except Exception as e:
        print(f"Exception occurred while creating user: {e}")
        return False


def auth_user(username, password, role=None):
    if username and password:
        # Tìm người dùng trong cơ sở dữ liệu theo username
        user = User.query.filter(User.username.__eq__(username.strip())).first()

        # Kiểm tra nếu tìm thấy người dùng và mật khẩu hợp lệ
        if user and user.password == password:
            # Nếu có role, kiểm tra role của người dùng
            if role and user.user_role == role:
                return user
            elif not role:  # Nếu không cần role, chỉ cần username và password đúng
                return user
    return None
