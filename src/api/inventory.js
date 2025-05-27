import apiClient from './index';

// 库存管理相关API
export default {
  // 库存API
  stock: {
    // 获取所有库存
    getAll(params = {}) {
      return apiClient.get('/inventory/stock/', { params });
    },
    
    // 获取单个商品库存
    getByProductId(productId) {
      return apiClient.get(`/inventory/stock/product/${productId}/`);
    },
    
    // 库存盘点
    check(data) {
      return apiClient.post('/inventory/stock/check/', data);
    }
  },
  
  // 库存变动记录API
  stockLogs: {
    // 获取所有库存变动记录
    getAll(params = {}) {
      return apiClient.get('/inventory/stock-logs/', { params });
    },
    
    // 获取单个商品的库存变动记录
    getByProductId(productId, params = {}) {
      return apiClient.get(`/inventory/stock-logs/product/${productId}/`, { params });
    }
  },
  
  // 库存预警API
  stockAlerts: {
    // 获取所有库存预警
    getAll() {
      return apiClient.get('/inventory/stock-alerts/');
    },
    
    // 获取单个商品的库存预警
    getByProductId(productId) {
      return apiClient.get(`/inventory/stock-alerts/product/${productId}/`);
    },
    
    // 设置库存预警阈值
    setThreshold(productId, minThreshold, maxThreshold) {
      return apiClient.post(`/inventory/stock-alerts/set-threshold/`, {
        product_id: productId,
        min_threshold: minThreshold,
        max_threshold: maxThreshold
      });
    }
  }
}; 