#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
创建前端环境配置文件
"""

# 创建生产环境配置文件
with open('coffee_front_end/.env.production', 'w', encoding='utf-8') as f:
    # 移除NODE_ENV，Vite不支持在.env文件中设置它
    f.write('VITE_API_URL=https://yucky-linet-huoyu2000-8e0fd916.koyeb.app/api\n')

# 创建开发环境配置文件
with open('coffee_front_end/.env.development', 'w', encoding='utf-8') as f:
    # 移除NODE_ENV，Vite不支持在.env文件中设置它
    f.write('VITE_API_URL=http://localhost:8000/api\n')

print('前端环境配置文件创建成功!') 