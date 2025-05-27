import apiClient from './index';

// 用户认证相关API
export default {
  // 用户登录
  login(username, password) {
    return apiClient.post('/auth/login/', { username, password });
  },
  
  // 用户登出
  logout() {
    const refreshToken = localStorage.getItem('refreshToken');
    return apiClient.post('/auth/logout/', { refresh: refreshToken });
  },
  
  // 刷新token
  refreshToken(refreshToken) {
    return apiClient.post('/auth/token/refresh/', { refresh: refreshToken });
  },
  
  // 获取当前用户信息
  getCurrentUser() {
    return apiClient.get('/auth/staff/me/');
  },
  
  // 修改密码
  changePassword(oldPassword, newPassword, confirmPassword) {
    return apiClient.post('/auth/staff/change_password/', {
      old_password: oldPassword,
      new_password: newPassword,
      confirm_password: confirmPassword
    });
  },

  // 角色管理API
  roles: {
    // 获取所有角色
    getAll() {
      return apiClient.get('/auth/roles/');
    },

    // 获取单个角色
    getById(id) {
      return apiClient.get(`/auth/roles/${id}/`);
    },

    // 创建角色
    create(data) {
      return apiClient.post('/auth/roles/', data);
    },

    // 更新角色
    update(id, data) {
      return apiClient.put(`/auth/roles/${id}/`, data);
    },

    // 删除角色
    delete(id) {
      return apiClient.delete(`/auth/roles/${id}/`);
    },

    // 获取角色权限
    getPermissions(id) {
      return apiClient.get(`/auth/roles/${id}/permissions/`);
    },

    // 添加权限到角色
    addPermission(id, permId) {
      return apiClient.post(`/auth/roles/${id}/add_permission/`, { perm_id: permId });
    },

    // 从角色移除权限
    removePermission(id, permId) {
      return apiClient.post(`/auth/roles/${id}/remove_permission/`, { perm_id: permId });
    }
  },

  // 权限管理API
  permissions: {
    // 获取所有权限
    getAll() {
      return apiClient.get('/auth/permissions/');
    }
  },

  // 用户管理API
  staff: {
    // 获取所有用户
    getAll() {
      return apiClient.get('/auth/staff/');
    },

    // 获取单个用户
    getById(id) {
      return apiClient.get(`/auth/staff/${id}/`);
    },

    // 创建用户
    create(data) {
      return apiClient.post('/auth/staff/', data);
    },

    // 更新用户
    update(id, data) {
      return apiClient.put(`/auth/staff/${id}/`, data);
    },

    // 删除用户
    delete(id) {
      return apiClient.delete(`/auth/staff/${id}/`);
    },

    // 重置密码
    resetPassword(id, newPassword) {
      return apiClient.post(`/auth/staff/${id}/reset_password/`, { 
        new_password: newPassword 
      });
    }
  },

  // 操作日志API
  logs: {
    // 获取操作日志
    getOperationLogs(params = {}) {
      return apiClient.get('/auth/operation-logs/', { params });
    }
  }
}; 