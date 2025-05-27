#!/bin/bash

echo "--- start.sh script initiated ---"

# 显示环境信息
echo "--- Environment Information ---"
echo "PORT (from env): $PORT"
# Set a default for PORT if not provided, though Koyeb should provide it
export PORT=${PORT:-8000}
echo "Effective PORT: $PORT"
echo "ALLOWED_HOSTS: $ALLOWED_HOSTS"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "Current directory: $(pwd)"

# 检查并显示Python和Django版本
echo "--- Python and Django Information ---"
if command -v python &> /dev/null; then
    python --version
    python -c "import django; print(f'Django version: {django.__version__}')"
else
    echo "Python command not found! Exiting."
    exit 1
fi

# 检查Gunicorn
echo "--- Gunicorn Information ---"
if command -v gunicorn &> /dev/null; then
    echo "Gunicorn path: $(command -v gunicorn)"
    gunicorn --version
else
    echo "Gunicorn command not found! Exiting."
    exit 1
fi

# 应用数据库迁移
echo "--- Applying Database Migrations ---"
python manage.py migrate --noinput
if [ $? -ne 0 ]; then
    echo "Database migration failed! Exiting."
    exit 1
fi

# 收集静态文件
echo "--- Collecting Static Files ---"
python manage.py collectstatic --noinput --clear
if [ $? -ne 0 ]; then
    echo "Collect static files failed! Exiting."
    exit 1
fi

# Gunicorn配置检查
echo "--- Checking Gunicorn Configuration ---"
# Hardcoded Gunicorn args for testing
GUNICORN_WORKERS=2
GUNICORN_THREADS=4
GUNICORN_TIMEOUT=120
GUNICORN_LOG_LEVEL="debug"

echo "Gunicorn check command: gunicorn coffee_shop_management.wsgi:application --bind 0.0.0.0:$PORT --workers $GUNICORN_WORKERS --threads $GUNICORN_THREADS --timeout $GUNICORN_TIMEOUT --log-level $GUNICORN_LOG_LEVEL --check-config --access-logfile='-' --error-logfile='-'"
gunicorn coffee_shop_management.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers "$GUNICORN_WORKERS" \
    --threads "$GUNICORN_THREADS" \
    --timeout "$GUNICORN_TIMEOUT" \
    --log-level "$GUNICORN_LOG_LEVEL" \
    --check-config \
    --access-logfile="-" \
    --error-logfile="-"

if [ $? -ne 0 ]; then
    echo "Gunicorn configuration check failed! Exiting."
    exit 1
else
    echo "Gunicorn configuration check passed."
fi

# 启动Gunicorn服务器
echo "--- Starting Gunicorn Server ---"
echo "Attempting to start Gunicorn on 0.0.0.0:$PORT with WSGI app: coffee_shop_management.wsgi:application"
echo "Full Gunicorn command: exec gunicorn coffee_shop_management.wsgi:application --bind 0.0.0.0:$PORT --workers $GUNICORN_WORKERS --threads $GUNICORN_THREADS --timeout $GUNICORN_TIMEOUT --log-level $GUNICORN_LOG_LEVEL --access-logfile='-' --error-logfile='-'"

exec gunicorn coffee_shop_management.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers "$GUNICORN_WORKERS" \
    --threads "$GUNICORN_THREADS" \
    --timeout "$GUNICORN_TIMEOUT" \
    --log-level "$GUNICORN_LOG_LEVEL" \
    --access-logfile="-" \
    --error-logfile="-"

# 如果Gunicorn启动失败或退出，下面的代码会被执行
echo "Gunicorn failed to start or exited unexpectedly! Exiting."
exit 1 