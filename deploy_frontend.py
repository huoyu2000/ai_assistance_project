#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
前端部署脚本
"""

import os
import subprocess
import sys

def run_command(command):
    """运行命令并打印输出"""
    print(f"执行命令: {command}")
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            sys.stdout.write(output.decode('utf-8'))
            sys.stdout.flush()
    
    return process.poll()

def main():
    """主函数"""
    # 切换到前端目录
    os.chdir('coffee_front_end')
    
    # 确保环境变量文件存在
    if not os.path.exists('.env.production'):
        print("创建环境变量文件...")
        with open('.env.production', 'w', encoding='utf-8') as f:
            f.write('VITE_API_URL=https://yucky-linet-huoyu2000-8e0fd916.koyeb.app/api\n')
    
    # 安装依赖
    print("安装依赖...")
    run_command("npm install")
    
    # 构建项目
    print("\n构建项目...")
    run_command("npm run build")
    
    print("\n前端构建完成！")
    print("dist目录已准备好，可以部署到Vercel、Netlify或其他静态网站托管服务。")
    print("\n部署提示:")
    print("1. 使用Vercel CLI: vercel --prod")
    print("2. 使用Netlify CLI: netlify deploy --prod")
    print("3. 或者直接将dist目录上传到您的静态网站托管服务")

if __name__ == "__main__":
    main() 