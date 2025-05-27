import { defineStore } from 'pinia';
import authApi from '../api/auth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    refreshToken: localStorage.getItem('refreshToken') || null,
    loading: false,
    error: null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },

  actions: {
    async login(username, password) {
      this.loading = true;
      this.error = null;
      try {
        const response = await authApi.login(username, password);
        this.token = response.access;
        this.refreshToken = response.refresh;
        localStorage.setItem('token', response.access);
        localStorage.setItem('refreshToken', response.refresh);
        await this.fetchCurrentUser();
        return true;
      } catch (error) {
        this.error = error.response?.data?.detail || '登录失败，请检查用户名和密码';
        return false;
      } finally {
        this.loading = false;
      }
    },

    async logout() {
      try {
        if (this.refreshToken) {
          await authApi.logout();
        }
      } catch (error) {
        console.error('登出时发生错误:', error);
      } finally {
        this.clearAuth();
      }
    },

    clearAuth() {
      this.user = null;
      this.token = null;
      this.refreshToken = null;
      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
    },

    async fetchCurrentUser() {
      if (!this.token) return;
      
      this.loading = true;
      try {
        const userData = await authApi.getCurrentUser();
        this.user = userData;
      } catch (error) {
        console.error('获取用户信息失败:', error);
        if (error.response?.status === 401) {
          this.clearAuth();
        }
      } finally {
        this.loading = false;
      }
    },

    async refreshAuthToken() {
      if (!this.refreshToken) return false;
      
      try {
        const response = await authApi.refreshToken(this.refreshToken);
        this.token = response.access;
        localStorage.setItem('token', response.access);
        return true;
      } catch (error) {
        console.error('刷新令牌失败:', error);
        this.clearAuth();
        return false;
      }
    }
  }
}); 