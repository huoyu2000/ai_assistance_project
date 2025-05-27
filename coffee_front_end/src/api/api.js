import authApi from './auth';
import productApi from './product';
import salesApi from './sales';
import inventoryApi from './inventory';
import purchaseApi from './purchase';
import financeApi from './finance';

// API入口文件
export default {
  auth: authApi,
  product: productApi,
  sales: salesApi,
  inventory: inventoryApi,
  purchase: purchaseApi,
  finance: financeApi
}; 