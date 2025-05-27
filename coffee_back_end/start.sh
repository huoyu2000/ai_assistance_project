#!/bin/bash

# 应用数据库迁移
echo "Applying database migrations..."
python manage.py migrate --noinput

# 收集静态文件
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 启动Gunicorn服务器
echo "Starting Gunicorn server..."
gunicorn coffee_shop_management.wsgi:application --bind 0.0.0.0:$PORT --log-level debug 