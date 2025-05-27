#!/bin/bash

set -e
set -x

echo "--- start.sh script initiated (v2) ---"
sleep 2 # Give logs a chance to flush

# 显示环境信息
echo "--- Environment Information ---"
echo "PORT (from env): $PORT"
# Set a default for PORT if not provided, though Koyeb should provide it
export PORT=${PORT:-8000}
echo "Effective PORT: $PORT"
echo "ALLOWED_HOSTS: $ALLOWED_HOSTS"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "Current directory: $(pwd)"
ls -la

# 检查并显示Python和Django版本
echo "--- Python and Django Information ---"
python --version
python -c "import django; print(f'Django version: {django.__version__}')"

# 检查Gunicorn
echo "--- Gunicorn Information ---"
gunicorn --version

# 应用数据库迁移
echo "--- Applying Database Migrations ---"
python manage.py migrate --noinput

# 收集静态文件
echo "--- Collecting Static Files ---"
python manage.py collectstatic --noinput --clear

# Gunicorn配置检查 (Simplified for now)
echo "--- Checking Gunicorn Configuration (Simplified) ---"
BASIC_GUNICORN_CHECK_CMD="gunicorn coffee_shop_management.wsgi:application --bind 0.0.0.0:$PORT --check-config --log-level=debug --error-logfile=-"
echo "Gunicorn check command: $BASIC_GUNICORN_CHECK_CMD"
$BASIC_GUNICORN_CHECK_CMD
echo "Gunicorn configuration check completed."


# 启动Gunicorn服务器 (Simplified command for testing)
echo "--- Starting Gunicorn Server (Simplified) ---"
# Basic Gunicorn arguments for testing
GUNICORN_WORKERS_TEST=1
GUNICORN_TIMEOUT_TEST=120
GUNICORN_LOG_LEVEL_TEST="debug"

FINAL_GUNICORN_CMD="exec gunicorn coffee_shop_management.wsgi:application --bind 0.0.0.0:$PORT --workers $GUNICORN_WORKERS_TEST --timeout $GUNICORN_TIMEOUT_TEST --log-level $GUNICORN_LOG_LEVEL_TEST --access-logfile='-' --error-logfile='-'"
echo "Final Gunicorn command: $FINAL_GUNICORN_CMD"

$FINAL_GUNICORN_CMD

# 如果Gunicorn启动失败或退出，下面的代码会被执行
echo "Gunicorn failed to start or exited unexpectedly! Exiting from start.sh."
exit 1 