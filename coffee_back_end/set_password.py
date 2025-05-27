#!/usr/bin/env python
import os
import sys
import django
from django.contrib.auth.hashers import make_password

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffee_shop_management.settings')
django.setup()

# 导入模型
from user_auth.models import Staff
from django.db import connection

def set_admin_password():
    """为admin用户设置密码"""
    try:
        # 直接使用SQL更新密码，避免ORM的验证问题
        with connection.cursor() as cursor:
            # 生成密码哈希
            password_hash = make_password('admin123')
            # 更新admin用户的密码
            cursor.execute(
                "UPDATE users SET password_hash = %s WHERE username = %s",
                [password_hash, 'admin']
            )
            print(f"已为admin用户设置密码: admin123")
    except Exception as e:
        print(f"设置密码时出错: {e}")

if __name__ == "__main__":
    set_admin_password() 