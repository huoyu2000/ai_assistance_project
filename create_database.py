import pymysql

# 数据库连接参数
host = 'localhost'
user = 'root'
password = '123123'

# 创建数据库连接
conn = pymysql.connect(host=host, user=user, password=password)
cursor = conn.cursor()

try:
    # 创建数据库
    cursor.execute("CREATE DATABASE IF NOT EXISTS coffee_shop_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    print("数据库 coffee_shop_db 创建成功")
finally:
    # 关闭连接
    cursor.close()
    conn.close() 