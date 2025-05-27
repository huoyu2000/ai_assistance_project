#!/bin/bash

# 显示环境信息
echo "Environment: PORT=$PORT, ALLOWED_HOSTS=$ALLOWED_HOSTS"
echo "Current directory: $(pwd)"
echo "Python version: $(python --version)"
echo "Django version: $(python -c 'import django; print(django.__version__)')"

# 应用数据库迁移
echo "Applying database migrations..."
python manage.py migrate --noinput

# 收集静态文件
echo "Collecting static files..."
python manage.py collectstatic --noinput

# 启动Gunicorn服务器
echo "Starting Gunicorn server on 0.0.0.0:$PORT..."
exec gunicorn coffee_shop_management.wsgi:application --bind 0.0.0.0:$PORT --log-level debug --timeout 120 