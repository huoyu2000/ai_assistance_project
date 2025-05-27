import apiClient from './index';

// 商品管理相关API
export default {
  // 商品分类API
  categories: {
    // 获取所有分类
    getAll() {
      return apiClient.get('/product/categories/');
    },
    
    // 获取单个分类
    getById(id) {
      return apiClient.get(`/product/categories/${id}/`);
    },
    
    // 创建分类
    create(data) {
      return apiClient.post('/product/categories/', data);
    },
    
    // 更新分类
    update(id, data) {
      return apiClient.put(`/product/categories/${id}/`, data);
    },
    
    // 删除分类
    delete(id) {
      return apiClient.delete(`/product/categories/${id}/`);
    }
  },
  
  // 商品API
  products: {
    // 获取所有商品
    getAll(params = {}) {
      return apiClient.get('/product/products/', { params });
    },
    
    // 获取单个商品
    getById(id) {
      return apiClient.get(`/product/products/${id}/`);
    },
    
    // 创建商品
    create(data) {
      return apiClient.post('/product/products/', data);
    },
    
    // 更新商品
    update(id, data) {
      return apiClient.put(`/product/products/${id}/`, data);
    },
    
    // 删除商品
    delete(id) {
      return apiClient.delete(`/product/products/${id}/`);
    }
  }
}; 