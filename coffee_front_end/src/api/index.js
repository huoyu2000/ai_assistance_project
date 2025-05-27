import axios from 'axios';

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

// 响应拦截器
apiClient.interceptors.response.use(
  response => {
    console.log(`API响应成功: ${response.config.method.toUpperCase()} ${response.config.url}`, response.data);
    return response.data;
  },
  error => {
    // 处理错误
    if (error.response) {
      console.error(`API响应错误 ${error.response.status}: ${error.config.method.toUpperCase()} ${error.config.url}`, error.response.data);
      
      // 处理401错误，token失效
      if (error.response.status === 401) {
        console.warn('认证失败，清除token并重定向到登录页面');
        localStorage.removeItem('token');
        localStorage.removeItem('refreshToken');
        window.location.href = '/login';
      }
    } else if (error.request) {
      console.error('API请求发送但未收到响应', error.request);
    } else {
      console.error('API请求设置错误', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default apiClient; 