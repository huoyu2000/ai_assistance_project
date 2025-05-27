FROM python:3.13-slim

WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV ALLOWED_HOSTS=".koyeb.app,localhost,127.0.0.1,0.0.0.0"
ENV DEBUG=False
ENV DJANGO_SETTINGS_MODULE=coffee_shop_management.settings

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 设置脚本权限
RUN chmod +x start.sh

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 暴露端口
EXPOSE $PORT

# 启动命令
CMD ["./start.sh"] 