import apiClient from './index';

// 销售管理相关API
export default {
  // 销售订单API
  orders: {
    // 获取所有销售订单
    getAll(params = {}) {
      return apiClient.get('/sales/orders/', { params });
    },
    
    // 获取单个销售订单
    getById(id) {
      return apiClient.get(`/sales/orders/${id}/`);
    },
    
    // 获取客户的所有订单
    getByCustomerId(customerId) {
      return apiClient.get(`/sales/customers/${customerId}/orders/`);
    },
    
    // 创建销售订单
    create(data) {
      return apiClient.post('/sales/orders/', data);
    },
    
    // 更新销售订单
    update(id, data) {
      return apiClient.put(`/sales/orders/${id}/`, data);
    },
    
    // 删除销售订单
    delete(id) {
      return apiClient.delete(`/sales/orders/${id}/`);
    },
    
    // 完成销售订单
    complete(id) {
      return apiClient.post(`/sales/orders/${id}/complete/`);
    },
    
    // 取消销售订单
    cancel(id) {
      return apiClient.post(`/sales/orders/${id}/cancel/`);
    }
  },
  
  // 销售订单项API
  orderItems: {
    // 获取订单所有项目
    getByOrderId(orderId) {
      return apiClient.get(`/sales/orders/${orderId}/items/`);
    },
    
    // 添加订单项目
    create(orderId, data) {
      return apiClient.post(`/sales/orders/${orderId}/items/`, data);
    },
    
    // 更新订单项目
    update(orderId, itemId, data) {
      return apiClient.put(`/sales/orders/${orderId}/items/${itemId}/`, data);
    },
    
    // 删除订单项目
    delete(orderId, itemId) {
      return apiClient.delete(`/sales/orders/${orderId}/items/${itemId}/`);
    }
  },
  
  // 客户API
  customers: {
    // 获取所有客户
    getAll(params = {}) {
      return apiClient.get('/sales/customers/', { params });
    },
    
    // 获取单个客户
    getById(id) {
      return apiClient.get(`/sales/customers/${id}/`);
    },
    
    // 创建客户
    create(data) {
      return apiClient.post('/sales/customers/', data);
    },
    
    // 更新客户
    update(id, data) {
      return apiClient.put(`/sales/customers/${id}/`, data);
    },
    
    // 删除客户
    delete(id) {
      return apiClient.delete(`/sales/customers/${id}/`);
    }
  },
  
  // 销售统计API
  statistics: {
    // 获取日销售统计
    getDaily(date) {
      return apiClient.get('/sales/statistics/daily/', { params: { date } });
    },
    
    // 获取月销售统计
    getMonthly(year, month) {
      return apiClient.get('/sales/statistics/monthly/', { params: { year, month } });
    },
    
    // 获取年销售统计
    getYearly(year) {
      return apiClient.get('/sales/statistics/yearly/', { params: { year } });
    },
    
    // 获取商品销售排名
    getProductRanking(params = {}) {
      return apiClient.get('/sales/statistics/product-ranking/', { params });
    }
  }
}; 