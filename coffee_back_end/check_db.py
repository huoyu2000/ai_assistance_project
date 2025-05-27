#!/usr/bin/env python
import os
import sys
import django

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coffee_shop_management.settings')
django.setup()

# 导入模型
from user_auth.models import Staff
from django.db import connection

# 获取数据库中表的结构
with connection.cursor() as cursor:
    # 获取users表的结构
    cursor.execute("DESCRIBE users")
    users_table = cursor.fetchall()
    print("users表结构:")
    for field in users_table:
        print(field)
    
    # 检查是否有用户
    cursor.execute("SELECT * FROM users LIMIT 5")
    users = cursor.fetchall()
    print("\n用户数据:")
    for user in users:
        print(user) 