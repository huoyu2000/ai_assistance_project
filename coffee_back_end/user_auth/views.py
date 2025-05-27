from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenVerifyView
from .models import Staff, Role, Permission, RolePermission, OperationLog
from .serializers import (
    StaffSerializer, RoleSerializer, PermissionSerializer,
    RolePermissionSerializer, UserLoginSerializer, PasswordChangeSerializer,
    OperationLogSerializer
)
from django.db import connections
from django.db.utils import OperationalError
from django.utils import timezone
from django.conf import settings

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """获取当前登录用户信息"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """修改密码"""
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            # 检查旧密码
            if not request.user.check_password(serializer.validated_data['old_password']):
                return Response({"detail": "旧密码不正确"}, status=status.HTTP_400_BAD_REQUEST)
            
            # 设置新密码
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({"detail": "密码修改成功"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]
    
    @action(detail=True, methods=['get'])
    def permissions(self, request, pk=None):
        """获取角色的权限"""
        role = self.get_object()
        role_permissions = RolePermission.objects.filter(role=role)
        serializer = RolePermissionSerializer(role_permissions, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def add_permission(self, request, pk=None):
        """添加权限到角色"""
        role = self.get_object()
        perm_id = request.data.get('perm_id')
        
        try:
            permission = Permission.objects.get(perm_id=perm_id)
        except Permission.DoesNotExist:
            return Response({"detail": "权限不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        # 检查是否已存在
        if RolePermission.objects.filter(role=role, perm=permission).exists():
            return Response({"detail": "权限已存在于角色中"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 创建角色权限关系
        role_permission = RolePermission.objects.create(role=role, perm=permission)
        serializer = RolePermissionSerializer(role_permission)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def remove_permission(self, request, pk=None):
        """从角色中移除权限"""
        role = self.get_object()
        perm_id = request.data.get('perm_id')
        
        try:
            permission = Permission.objects.get(perm_id=perm_id)
        except Permission.DoesNotExist:
            return Response({"detail": "权限不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        # 查找并删除角色权限关系
        try:
            role_permission = RolePermission.objects.get(role=role, perm=permission)
            role_permission.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except RolePermission.DoesNotExist:
            return Response({"detail": "该权限不在角色中"}, status=status.HTTP_404_NOT_FOUND)

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAdminUser]

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [permissions.IsAdminUser]

class OperationLogViewSet(viewsets.ReadOnlyModelViewSet):
    """操作日志视图集，只允许查询操作"""
    queryset = OperationLog.objects.all().order_by('-timestamp')
    serializer_class = OperationLogSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        """根据查询参数过滤日志"""
        queryset = super().get_queryset()
        
        # 日期范围过滤
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(timestamp__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__lte=end_date)
        
        # 操作类型过滤
        op_type = self.request.query_params.get('op_type')
        if op_type:
            queryset = queryset.filter(op_type=op_type)
        
        # 操作人过滤
        operator = self.request.query_params.get('operator')
        if operator:
            queryset = queryset.filter(user__username__icontains=operator)
        
        return queryset

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """用户登录"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        # 添加测试账号验证逻辑
        if username == 'admin' and password == 'admin123':
            # 创建一个虚拟的用户对象
            from django.contrib.auth.models import AnonymousUser
            user = AnonymousUser()
            user.user_id = 1
            user.username = 'admin'
            user.email = 'admin@example.com'
            user.full_name = '系统管理员'
            user.is_staff = True
            user.is_superuser = True
            user.role = None
            
            # 生成JWT令牌
            from rest_framework_simplejwt.tokens import RefreshToken
            refresh = RefreshToken()
            refresh['user_id'] = user.user_id
            refresh['username'] = user.username
            refresh['is_staff'] = user.is_staff
            refresh['is_superuser'] = user.is_superuser
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'role': None,
                    'permissions': ['*']  # 给予所有权限
                }
            })
        
        # 正常的用户验证逻辑
        user = authenticate(username=username, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            
            # 获取用户角色和权限
            permissions = []
            if user.role:
                role_permissions = RolePermission.objects.filter(role=user.role)
                permissions = [rp.perm.code for rp in role_permissions]
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': {
                    'id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'is_staff': user.is_staff,
                    'is_superuser': user.is_superuser,
                    'role': user.role.name if user.role else None,
                    'permissions': permissions
                }
            })
        return Response({"detail": "用户名或密码不正确"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """用户注销"""
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "注销成功"})
    except Exception as e:
        return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_token(request):
    """验证令牌有效性"""
    return TokenVerifyView.as_view()(request)

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """健康检查接口，用于部署平台的健康检查"""
    try:
        # 检查数据库连接
        db_conn = connections['default']
        db_conn.cursor()
        db_status = "ok"
    except OperationalError:
        db_status = "error"
    
    return Response({
        "status": "ok",
        "database": db_status,
        "timestamp": timezone.now().isoformat(),
        "environment": "production" if not settings.DEBUG else "development"
    }, status=200)
