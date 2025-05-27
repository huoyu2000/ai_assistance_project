from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class Role(models.Model):
    """用户角色模型"""
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=128, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        managed = False
        db_table = 'roles'
        verbose_name = '角色'
        verbose_name_plural = '角色'
    
    def __str__(self):
        return str(self.name)

class Permission(models.Model):
    """权限模型"""
    perm_id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=64)
    
    class Meta:
        managed = False
        db_table = 'permissions'
        verbose_name = '权限'
        verbose_name_plural = '权限'
    
    def __str__(self):
        return str(self.name)

class RolePermission(models.Model):
    """角色权限关联模型"""
    role = models.ForeignKey(Role, models.CASCADE, primary_key=True)
    perm = models.ForeignKey(Permission, models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'role_permission'
        verbose_name = '角色权限'
        verbose_name_plural = '角色权限'
        unique_together = (('role', 'perm'),)
    
    def __str__(self):
        return f"{self.role.name} - {self.perm.name}"

class StaffManager(BaseUserManager):
    """自定义用户管理器，处理用户表的主键名不同等情况"""
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        if not username:
            raise ValueError('用户名不能为空')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('status', 'ACTIVE')
        return self.create_user(username, email, password, **extra_fields)

class Staff(AbstractBaseUser, PermissionsMixin):
    """员工模型，映射到users表"""
    USER_STATUS_CHOICES = [
        ('ACTIVE', '活跃'),
        ('DISABLED', '禁用')
    ]
    
    user_id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True)
    full_name = models.CharField(max_length=32, null=True, blank=True)
    email = models.CharField(max_length=64, null=True, blank=True)
    password_hash = models.CharField(max_length=128)
    role = models.ForeignKey(Role, models.SET_NULL, null=True, blank=True, db_column='role_id')
    status = models.CharField(max_length=8, choices=USER_STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # 这些字段在数据库中不存在，但Django需要它们
    first_name = None
    last_name = None
    last_login = None  # 移除last_login字段
    
    objects = StaffManager()
    
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        managed = False
        db_table = 'users'
        verbose_name = '员工'
        verbose_name_plural = '员工'
    
    def __str__(self):
        return f"{self.username} ({self.full_name or ''})"
    
    # 重写password属性，映射到password_hash
    @property
    def password(self):
        return self.password_hash
    
    @password.setter
    def password(self, value):
        self.password_hash = value
    
    # 基于status字段的属性
    @property
    def is_active(self):
        return self.status == 'ACTIVE'
    
    @property
    def is_staff(self):
        if not self.role:
            return False
        # 获取role_id，因为role是ForeignKey
        role_id = self.role.role_id
        return role_id == 1 or role_id == 2
    
    @property
    def is_superuser(self):
        if not self.role:
            return False
        # 获取role_id，因为role是ForeignKey
        role_id = self.role.role_id
        return role_id == 1
    
    def get_full_name(self):
        return self.full_name or self.username
    
    def get_short_name(self):
        return self.username
    
    # 为了兼容Django的权限系统
    def has_perm(self, perm, obj=None):
        return self.is_active and (self.is_staff or self.is_superuser)
    
    def has_module_perms(self, app_label):
        return self.is_active and (self.is_staff or self.is_superuser)

class LoginLog(models.Model):
    """登录日志模型"""
    user = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='login_logs', verbose_name='用户')
    login_time = models.DateTimeField(auto_now_add=True, verbose_name='登录时间')
    logout_time = models.DateTimeField(blank=True, null=True, verbose_name='登出时间')
    ip_address = models.GenericIPAddressField(verbose_name='IP地址')
    user_agent = models.TextField(verbose_name='浏览器信息')
    is_successful = models.BooleanField(default=True, verbose_name='是否成功')
    
    class Meta:
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name
        ordering = ['-login_time']
    
    def __str__(self):
        user_name = self.user.username if hasattr(self.user, 'username') else 'Unknown'
        return f"{user_name} - {self.login_time}"

class OperationLog(models.Model):
    """操作日志模型"""
    OP_TYPES = [
        ('LOGIN', '登录'),
        ('CREATE', '创建'),
        ('UPDATE', '更新'),
        ('DELETE', '删除'),
    ]
    
    log_id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(Staff, models.CASCADE, db_column='user_id')
    ip_addr = models.CharField(max_length=45)
    op_type = models.CharField(max_length=10, choices=OP_TYPES)
    entity = models.CharField(max_length=64)
    details = models.TextField(null=True, blank=True)
    
    class Meta:
        managed = False
        db_table = 'operation_logs'
        verbose_name = '操作日志'
        verbose_name_plural = '操作日志'
        ordering = ['-timestamp']
    
    def __str__(self):
        user_name = self.user.username if hasattr(self.user, 'username') else 'Unknown'
        return f"{self.timestamp} - {user_name} - {self.op_type}"
