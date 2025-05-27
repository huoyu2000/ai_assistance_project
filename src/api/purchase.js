import apiClient from './index';

// 采购管理相关API
export default {
  // 供应商API
  suppliers: {
    // 获取所有供应商
    getAll() {
      return apiClient.get('/purchase/suppliers/');
    },
    
    // 获取单个供应商
    getById(id) {
      return apiClient.get(`/purchase/suppliers/${id}/`);
    },
    
    // 创建供应商
    create(data) {
      return apiClient.post('/purchase/suppliers/', data);
    },
    
    // 更新供应商
    update(id, data) {
      return apiClient.put(`/purchase/suppliers/${id}/`, data);
    },
    
    // 删除供应商
    delete(id) {
      return apiClient.delete(`/purchase/suppliers/${id}/`);
    }
  },
  
  // 采购订单API
  orders: {
    // 获取所有采购订单
    getAll(params = {}) {
      return apiClient.get('/purchase/orders/', { params });
    },
    
    // 获取单个采购订单
    getById(id) {
      return apiClient.get(`/purchase/orders/${id}/`);
    },
    
    // 创建采购订单
    create(data) {
      return apiClient.post('/purchase/orders/', data);
    },
    
    // 更新采购订单
    update(id, data) {
      return apiClient.put(`/purchase/orders/${id}/`, data);
    },
    
    // 删除采购订单
    delete(id) {
      return apiClient.delete(`/purchase/orders/${id}/`);
    },
    
    // 确认采购订单
    confirm(id) {
      return apiClient.post(`/purchase/orders/${id}/confirm/`);
    },
    
    // 取消采购订单
    cancel(id) {
      return apiClient.post(`/purchase/orders/${id}/cancel/`);
    }
  },
  
  // 采购订单项API
  orderItems: {
    // 获取订单所有项目
    getByOrderId(orderId) {
      return apiClient.get(`/purchase/orders/${orderId}/items/`);
    },
    
    // 添加订单项目
    create(orderId, data) {
      return apiClient.post(`/purchase/orders/${orderId}/items/`, data);
    },
    
    // 更新订单项目
    update(orderId, itemId, data) {
      return apiClient.put(`/purchase/orders/${orderId}/items/${itemId}/`, data);
    },
    
    // 删除订单项目
    delete(orderId, itemId) {
      return apiClient.delete(`/purchase/orders/${orderId}/items/${itemId}/`);
    }
  }
}; 