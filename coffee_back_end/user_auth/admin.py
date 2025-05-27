from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Staff, Role, Permission, RolePermission, OperationLog

class StaffAdmin(admin.ModelAdmin):
    """自定义员工管理界面"""
    list_display = ('username', 'full_name', 'get_role', 'email', 'status', 'get_is_active')
    list_filter = ('status', 'role')
    search_fields = ('username', 'full_name', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'password_hash')}),
        ('个人信息', {'fields': ('full_name', 'email', 'role')}),
        ('状态', {'fields': ('status',)}),
        ('重要日期', {'fields': ('created_at',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password_hash', 'role'),
        }),
    )
    
    def get_role(self, obj):
        return obj.role.name if obj.role else '-'
    get_role.short_description = '角色'
    get_role.admin_order_field = 'role__name'
    
    def get_is_active(self, obj):
        return obj.is_active
    get_is_active.short_description = '是否活跃'
    get_is_active.boolean = True

class RolePermissionInline(admin.TabularInline):
    model = RolePermission
    extra = 1
    fk_name = 'role'

class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')
    inlines = [RolePermissionInline]

class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

admin.site.register(Staff, StaffAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Permission, PermissionAdmin)
admin.site.register(RolePermission)
admin.site.register(OperationLog)
