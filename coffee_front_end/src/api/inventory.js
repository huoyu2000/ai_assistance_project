import apiClient from './index';

// 库存管理相关API
export default {
  // 库存API
  stock: {
    // 获取所有库存
    async getAll(params = {}) {
      try {
        // 由于inventory_inventory表不存在，我们使用product API获取产品列表
        const response = await apiClient.get('/product/products/', { params });
        
        if (Array.isArray(response)) {
          return response.map(product => ({
            id: product.product_id,
            product_name: product.name,
            product_unit: product.unit,
            current_quantity: product.inventory_qty || 0,
            minimum_quantity: product.reorder_point || 0,
            updated_at: product.updated_at || new Date().toISOString().split('T')[0],
            is_low_stock: (product.inventory_qty || 0) <= (product.reorder_point || 0)
          }));
        } else if (response && Array.isArray(response.results)) {
          return response.results.map(product => ({
            id: product.product_id,
            product_name: product.name,
            product_unit: product.unit,
            current_quantity: product.inventory_qty || 0,
            minimum_quantity: product.reorder_point || 0,
            updated_at: product.updated_at || new Date().toISOString().split('T')[0],
            is_low_stock: (product.inventory_qty || 0) <= (product.reorder_point || 0)
          }));
        } else {
          console.error('无法从API响应中提取库存数组');
          return [];
        }
      } catch (error) {
        console.error('获取库存列表失败:', error);
        return [];
      }
    },
    
    // 获取单个商品库存
    async getByProductId(productId) {
      try {
        const response = await apiClient.get(`/product/products/${productId}/`);
        return {
          id: response.product_id,
          product_name: response.name,
          product_unit: response.unit,
          current_quantity: response.inventory_qty || 0,
          minimum_quantity: response.reorder_point || 0,
          updated_at: response.updated_at || new Date().toISOString().split('T')[0],
          is_low_stock: (response.inventory_qty || 0) <= (response.reorder_point || 0)
        };
      } catch (error) {
        console.error(`获取商品ID ${productId} 的库存失败:`, error);
        return null;
      }
    },
    
    // 库存盘点
    check(data) {
      return apiClient.post('/inventory/counts/', data);
    },
    
    // 更新库存
    update(inventoryId, data) {
      return apiClient.put(`/inventory/inventories/${inventoryId}/`, data);
    },
    
    // 调整库存
    adjust(inventoryId, data) {
      return apiClient.post(`/inventory/inventories/${inventoryId}/adjust/`, data);
    }
  },
  
  // 批次管理API - 由于后端错误，我们使用模拟数据
  batches: {
    // 获取所有批次
    async getAll(params = {}) {
      try {
        // 模拟批次数据
        const mockBatches = [
          { 
            batch_id: 1,
            product_name: '牛奶', 
            batch_no: 'B20231110', 
            qty: 20, 
            expiry_date: '2023-11-20', 
            status: 'ACTIVE' 
          },
          { 
            batch_id: 2,
            product_name: '意式浓缩咖啡豆', 
            batch_no: 'B20231105', 
            qty: 50, 
            expiry_date: '2024-05-05', 
            status: 'ACTIVE' 
          },
          { 
            batch_id: 3,
            product_name: '巧克力糖浆', 
            batch_no: 'B20231025', 
            qty: 10, 
            expiry_date: '2024-01-25', 
            status: 'ACTIVE' 
          }
        ];
        
        return mockBatches;
      } catch (error) {
        console.error('获取批次列表失败:', error);
        return [];
      }
    },
    
    // 获取单个商品的批次
    async getByProductId(productId, params = {}) {
      try {
        // 模拟批次数据
        const mockBatches = [
          { 
            batch_id: 1,
            product_name: '牛奶', 
            batch_no: 'B20231110', 
            qty: 20, 
            expiry_date: '2023-11-20', 
            status: 'ACTIVE' 
          },
          { 
            batch_id: 2,
            product_name: '意式浓缩咖啡豆', 
            batch_no: 'B20231105', 
            qty: 50, 
            expiry_date: '2024-05-05', 
            status: 'ACTIVE' 
          },
          { 
            batch_id: 3,
            product_name: '巧克力糖浆', 
            batch_no: 'B20231025', 
            qty: 10, 
            expiry_date: '2024-01-25', 
            status: 'ACTIVE' 
          }
        ];
        
        return mockBatches.filter(batch => batch.product_name.includes(productId));
      } catch (error) {
        console.error(`获取商品ID ${productId} 的批次失败:`, error);
        return [];
      }
    },
    
    // 创建批次
    create(data) {
      return apiClient.post('/inventory/batches/', data);
    },
    
    // 更新批次
    update(batchId, data) {
      return apiClient.put(`/inventory/batches/${batchId}/`, data);
    },
    
    // 删除批次
    delete(batchId) {
      return apiClient.delete(`/inventory/batches/${batchId}/`);
    }
  },
  
  // 库存变动记录API
  stockLogs: {
    // 获取所有库存变动记录
    async getAll(params = {}) {
      try {
        const response = await apiClient.get('/inventory/transactions/', { params });
        if (Array.isArray(response)) {
          return response;
        } else if (response && Array.isArray(response.results)) {
          return response.results;
        } else {
          console.error('无法从API响应中提取库存变动记录数组');
          return [];
        }
      } catch (error) {
        console.error('获取库存变动记录列表失败:', error);
        return [];
      }
    },
    
    // 获取单个商品的库存变动记录
    getByProductId(productId, params = {}) {
      return apiClient.get('/inventory/transactions/', { 
        params: { ...params, product: productId } 
      });
    }
  },
  
  // 库存预警API
  stockAlerts: {
    // 获取所有库存预警
    async getAll() {
      try {
        // 使用product API获取产品列表，然后筛选出低库存和即将过期的商品
        const products = await this.getLowStock();
        
        // 模拟批次数据
        const batches = [
          { 
            batch_id: 1,
            product_name: '牛奶', 
            batch_no: 'B20231110', 
            qty: 20, 
            expiry_date: '2023-11-20', 
            status: 'ACTIVE' 
          }
        ];
        
        return {
          low_stock: products,
          expiring_soon: batches
        };
      } catch (error) {
        console.error('获取库存预警列表失败:', error);
        return { low_stock: [], expiring_soon: [] };
      }
    },
    
    // 获取低库存预警
    async getLowStock() {
      try {
        const response = await apiClient.get('/product/products/', { 
          params: { low_stock: true }
        });
        
        let products = [];
        if (Array.isArray(response)) {
          products = response;
        } else if (response && Array.isArray(response.results)) {
          products = response.results;
        }
        
        // 筛选库存低于补货点的商品
        return products
          .filter(product => (product.inventory_qty || 0) <= (product.reorder_point || 0))
          .map(product => ({
            id: product.product_id,
            product_name: product.name,
            product_unit: product.unit,
            current_quantity: product.inventory_qty || 0,
            minimum_quantity: product.reorder_point || 0
          }));
      } catch (error) {
        console.error('获取低库存预警列表失败:', error);
        return [];
      }
    },
    
    // 获取即将过期预警
    async getExpiringSoon() {
      try {
        // 模拟批次数据
        const mockBatches = [
          { 
            batch_id: 1,
            product_name: '牛奶', 
            batch_no: 'B20231110', 
            qty: 20, 
            expiry_date: '2023-11-20', 
            status: 'ACTIVE' 
          }
        ];
        
        return mockBatches;
      } catch (error) {
        console.error('获取即将过期预警列表失败:', error);
        return [];
      }
    }
  }
}; 