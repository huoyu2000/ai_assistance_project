"""
WSGI config for coffee_shop_management project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# 添加项目根目录到Python路径
app_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.append(app_path)

# 设置Django设置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffee_shop_management.settings")

application = get_wsgi_application()
