#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
创建UTF-8编码的Procfile文件
"""

with open('coffee_back_end/Procfile', 'w', encoding='utf-8') as f:
    f.write('release: python manage.py initialize_db\n')
    f.write('web: gunicorn coffee_shop_management.wsgi --log-file -\n')

print('Procfile创建成功!') 