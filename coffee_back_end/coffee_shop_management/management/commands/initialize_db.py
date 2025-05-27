import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection

class Command(BaseCommand):
    help = '初始化数据库，执行迁移和加载初始数据'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('开始初始化数据库...'))
        
        # 检查数据库连接
        self.stdout.write('检查数据库连接...')
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                self.stdout.write(self.style.SUCCESS('数据库连接成功!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'数据库连接失败: {str(e)}'))
            return
        
        # 执行迁移
        self.stdout.write('执行数据库迁移...')
        try:
            call_command('migrate', interactive=False)
            self.stdout.write(self.style.SUCCESS('数据库迁移完成!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'数据库迁移失败: {str(e)}'))
            return
        
        # 收集静态文件
        self.stdout.write('收集静态文件...')
        try:
            call_command('collectstatic', interactive=False)
            self.stdout.write(self.style.SUCCESS('静态文件收集完成!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'静态文件收集失败: {str(e)}'))
        
        # 创建超级用户（如果不存在）
        self.stdout.write('检查超级用户...')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if not User.objects.filter(username='admin').exists():
            self.stdout.write('创建超级用户...')
            try:
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password=os.environ.get('ADMIN_PASSWORD', 'admin123456')
                )
                self.stdout.write(self.style.SUCCESS('超级用户创建成功!'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'创建超级用户失败: {str(e)}'))
        else:
            self.stdout.write('超级用户已存在，跳过创建')
        
        self.stdout.write(self.style.SUCCESS('数据库初始化完成!')) 