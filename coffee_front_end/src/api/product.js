import apiClient from './index';

// 商品管理相关API
export default {
  // 商品分类API
  categories: {
    // 获取所有分类
    async getAll() {
      try {
        const response = await apiClient.get('/product/categories/');
        // 确保返回的是数组
        if (Array.isArray(response)) {
          return response;
        } else if (response && typeof response === 'object') {
          // 如果是对象，尝试转换为数组
          console.log('API返回的分类数据不是数组，尝试转换:', response);
          if (Array.isArray(response.results)) {
            return response.results;
          } else {
            console.error('无法从API响应中提取分类数组');
            return [];
          }
        } else {
          console.error('API返回的分类数据格式不正确:', response);
          return [];
        }
      } catch (error) {
        console.error('获取分类列表失败:', error);
        return [];
      }
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
    async getAll(params = {}) {
      try {
        const response = await apiClient.get('/product/products/', { params });
        // 确保返回的是数组
        if (Array.isArray(response)) {
          return response;
        } else if (response && typeof response === 'object') {
          // 如果是对象，尝试转换为数组
          console.log('API返回的产品数据不是数组，尝试转换:', response);
          if (Array.isArray(response.results)) {
            return response.results;
          } else {
            console.error('无法从API响应中提取产品数组');
            return [];
          }
        } else {
          console.error('API返回的产品数据格式不正确:', response);
          return [];
        }
      } catch (error) {
        console.error('获取产品列表失败:', error);
        return [];
      }
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
    async update(id, data) {
      try {
        console.log(`更新产品 ID:${id}，发送数据:`, data);
        const response = await apiClient.put(`/product/products/${id}/`, data);
        console.log('API更新产品响应:', response);
        return response;
      } catch (error) {
        console.error('API更新产品错误:', error);
        throw error;
      }
    },
    
    // 删除商品
    delete(id) {
      return apiClient.delete(`/product/products/${id}/`);
    }
  }
}; 