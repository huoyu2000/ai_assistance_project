import apiClient from './index';

// 采购管理相关API
export default {
  // 供应商API
  suppliers: {
    // 获取所有供应商
    async getAll() {
      try {
        const response = await apiClient.get('/procurement/suppliers/');
        // 确保返回的是数组
        if (Array.isArray(response)) {
          return response;
        } else if (response && typeof response === 'object') {
          // 如果是对象，尝试转换为数组
          console.log('API返回的供应商数据不是数组，尝试转换:', response);
          if (Array.isArray(response.results)) {
            return response.results;
          } else {
            console.error('无法从API响应中提取供应商数组');
            return [];
          }
        } else {
          console.error('API返回的供应商数据格式不正确:', response);
          return [];
        }
      } catch (error) {
        console.error('获取供应商列表失败:', error);
        return [];
      }
    },
    
    // 获取单个供应商
    async getById(id) {
      try {
        return await apiClient.get(`/procurement/suppliers/${id}/`);
      } catch (error) {
        console.error(`获取供应商(ID: ${id})失败:`, error);
        throw error;
      }
    },
    
    // 创建供应商
    async create(data) {
      try {
        return await apiClient.post('/procurement/suppliers/', data);
      } catch (error) {
        console.error('创建供应商失败:', error);
        throw error;
      }
    },
    
    // 更新供应商
    async update(id, data) {
      try {
        return await apiClient.put(`/procurement/suppliers/${id}/`, data);
      } catch (error) {
        console.error(`更新供应商(ID: ${id})失败:`, error);
        throw error;
      }
    },
    
    // 删除供应商
    async delete(id) {
      try {
        return await apiClient.delete(`/procurement/suppliers/${id}/`);
      } catch (error) {
        console.error(`删除供应商(ID: ${id})失败:`, error);
        throw error;
      }
    },
    
    // 获取供应商的产品
    async getProducts(supplierId) {
      try {
        const response = await apiClient.get(`/procurement/suppliers/${supplierId}/products/`);
        if (Array.isArray(response)) {
          return response;
        } else if (response && Array.isArray(response.results)) {
          return response.results;
        } else {
          return [];
        }
      } catch (error) {
        console.error(`获取供应商(ID: ${supplierId})的产品失败:`, error);
        return [];
      }
    }
  },
  
  // 采购订单API
  orders: {
    // 获取所有采购订单
    async getAll(params = {}) {
      try {
        const response = await apiClient.get('/procurement/purchase-orders/', { params });
        if (Array.isArray(response)) {
          return response;
        } else if (response && Array.isArray(response.results)) {
          return response.results;
        } else {
          return [];
        }
      } catch (error) {
        console.error('获取采购订单列表失败:', error);
        return [];
      }
    },
    
    // 获取单个采购订单
    async getById(id) {
      try {
        return await apiClient.get(`/procurement/purchase-orders/${id}/`);
      } catch (error) {
        console.error(`获取采购订单(ID: ${id})失败:`, error);
        throw error;
      }
    },
    
    // 创建采购订单
    async create(data) {
      try {
        return await apiClient.post('/procurement/purchase-orders/', data);
      } catch (error) {
        console.error('创建采购订单失败:', error);
        throw error;
      }
    },
    
    // 更新采购订单
    async update(id, data) {
      try {
        return await apiClient.put(`/procurement/purchase-orders/${id}/`, data);
      } catch (error) {
        console.error(`更新采购订单(ID: ${id})失败:`, error);
        throw error;
      }
    },
    
    // 删除采购订单
    async delete(id) {
      try {
        return await apiClient.delete(`/procurement/purchase-orders/${id}/`);
      } catch (error) {
        console.error(`删除采购订单(ID: ${id})失败:`, error);
        throw error;
      }
    },
    
    // 确认采购订单
    async confirm(id) {
      try {
        return await apiClient.post(`/procurement/purchase-orders/${id}/confirm/`);
      } catch (error) {
        console.error(`确认采购订单(ID: ${id})失败:`, error);
        throw error;
      }
    },
    
    // 取消采购订单
    async cancel(id) {
      try {
        return await apiClient.post(`/procurement/purchase-orders/${id}/cancel/`);
      } catch (error) {
        console.error(`取消采购订单(ID: ${id})失败:`, error);
        throw error;
      }
    }
  },
  
  // 采购订单项API
  orderItems: {
    // 获取订单所有项目
    async getByOrderId(orderId) {
      try {
        const response = await apiClient.get(`/procurement/purchase-orders/${orderId}/items/`);
        if (Array.isArray(response)) {
          return response;
        } else if (response && Array.isArray(response.results)) {
          return response.results;
        } else {
          return [];
        }
      } catch (error) {
        console.error(`获取采购订单(ID: ${orderId})的项目失败:`, error);
        return [];
      }
    },
    
    // 添加订单项目
    async create(orderId, data) {
      try {
        return await apiClient.post(`/procurement/purchase-orders/${orderId}/items/`, data);
      } catch (error) {
        console.error(`添加采购订单(ID: ${orderId})项目失败:`, error);
        throw error;
      }
    },
    
    // 更新订单项目
    async update(orderId, itemId, data) {
      try {
        return await apiClient.put(`/procurement/purchase-orders/${orderId}/items/${itemId}/`, data);
      } catch (error) {
        console.error(`更新采购订单(ID: ${orderId})项目(ID: ${itemId})失败:`, error);
        throw error;
      }
    },
    
    // 删除订单项目
    async delete(orderId, itemId) {
      try {
        return await apiClient.delete(`/procurement/purchase-orders/${orderId}/items/${itemId}/`);
      } catch (error) {
        console.error(`删除采购订单(ID: ${orderId})项目(ID: ${itemId})失败:`, error);
        throw error;
      }
    }
  },
  
  // 供应商产品API
  supplierProducts: {
    // 获取所有供应商产品
    async getAll(params = {}) {
      try {
        const response = await apiClient.get('/procurement/supplier-products/', { params });
        if (Array.isArray(response)) {
          return response;
        } else if (response && Array.isArray(response.results)) {
          return response.results;
        } else {
          return [];
        }
      } catch (error) {
        console.error('获取供应商产品列表失败:', error);
        return [];
      }
    },
    
    // 获取单个供应商产品
    async getById(id) {
      try {
        return await apiClient.get(`/procurement/supplier-products/${id}/`);
      } catch (error) {
        console.error(`获取供应商产品(ID: ${id})失败:`, error);
        throw error;
      }
    },
    
    // 创建供应商产品
    async create(data) {
      try {
        return await apiClient.post('/procurement/supplier-products/', data);
      } catch (error) {
        console.error('创建供应商产品失败:', error);
        throw error;
      }
    },
    
    // 更新供应商产品
    async update(id, data) {
      try {
        return await apiClient.put(`/procurement/supplier-products/${id}/`, data);
      } catch (error) {
        console.error(`更新供应商产品(ID: ${id})失败:`, error);
        throw error;
      }
    },
    
    // 删除供应商产品
    async delete(id) {
      try {
        return await apiClient.delete(`/procurement/supplier-products/${id}/`);
      } catch (error) {
        console.error(`删除供应商产品(ID: ${id})失败:`, error);
        throw error;
      }
    }
  }
}; 