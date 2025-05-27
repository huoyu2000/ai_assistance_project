from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Staff, Role, Permission, RolePermission, OperationLog

User = get_user_model()

class StaffSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    
    class Meta:
        model = Staff
        fields = ['user_id', 'username', 'email', 'full_name', 'role', 'role_name',
                 'status', 'is_active', 'is_staff']
        extra_kwargs = {
            'password_hash': {'write_only': True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class RoleSerializer(serializers.ModelSerializer):
    userCount = serializers.SerializerMethodField()
    
    class Meta:
        model = Role
        fields = ['role_id', 'name', 'description', 'created_at', 'userCount']
    
    def get_userCount(self, obj):
        """计算每个角色关联的用户数量"""
        return Staff.objects.filter(role=obj).count()

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['perm_id', 'code', 'name']

class RolePermissionSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    permission_name = serializers.CharField(source='perm.name', read_only=True)
    permission_code = serializers.CharField(source='perm.code', read_only=True)
    
    class Meta:
        model = RolePermission
        fields = ['role', 'role_name', 'perm', 'permission_name', 'permission_code']

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, write_only=True, required=True)
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirm_password = serializers.CharField(max_length=128, write_only=True, required=True)
    
    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("新密码与确认密码不匹配")
        return data 

class OperationLogSerializer(serializers.ModelSerializer):
    """操作日志序列化器"""
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = OperationLog
        fields = ['log_id', 'timestamp', 'user', 'user_name', 'ip_addr', 'op_type', 'entity', 'details'] 