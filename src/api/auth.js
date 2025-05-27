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
  }
}; 