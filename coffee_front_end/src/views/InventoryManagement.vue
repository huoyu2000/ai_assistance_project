<template>
  <div class="page-content-container">
    <div class="header">
      <h1 class="page-title">库存管理</h1>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <!-- 错误提示 -->
    <div v-if="error" class="error-message">
      <p>{{ error }}</p>
      <button @click="fetchAllData" class="retry-button">重试</button>
    </div>

    <!-- 当前库存水平部分 -->
    <div v-if="!loading && !error" class="section-container">
      <h2 class="section-title">当前库存水平</h2>
      <div class="table-container">
        <table class="inventory-table">
          <thead>
            <tr>
              <th>项目</th>
              <th>类别</th>
              <th>库存水平</th>
              <th>单位</th>
              <th>补货点</th>
              <th>最后更新</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in inventoryItems" :key="index">
              <td>{{ item.name }}</td>
              <td class="text-secondary">{{ item.category }}</td>
              <td class="text-secondary" :class="{ 'text-warning': item.quantity <= item.reorderPoint }">{{ item.quantity }}</td>
              <td class="text-secondary">{{ item.unit }}</td>
              <td class="text-secondary">{{ item.reorderPoint }}</td>
              <td class="text-secondary">{{ item.lastUpdated }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 批次管理部分 -->
    <div v-if="!loading && !error" class="section-container">
      <h2 class="section-title">批次管理</h2>
      <div class="table-container">
        <table class="batch-table">
          <thead>
            <tr>
              <th>项目</th>
              <th>批次号</th>
              <th>数量</th>
              <th>到期日期</th>
              <th>状态</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(batch, index) in batchItems" :key="index">
              <td>{{ batch.name }}</td>
              <td class="text-secondary">{{ batch.batchNumber }}</td>
              <td class="text-secondary">{{ batch.quantity }}</td>
              <td class="text-secondary" :class="{ 'text-warning': isExpirationNear(batch.expirationDate) }">{{ batch.expirationDate }}</td>
              <td>
                <span class="status-badge" :class="{ 'inactive': batch.status !== '活跃' }">
                  {{ batch.status }}
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 库存预警部分 -->
    <div v-if="!loading && !error" class="section-container">
      <h2 class="section-title">库存预警</h2>
      <div class="alert-container">
        <div v-if="lowStockItems.length > 0" class="alert-card">
          <h3 class="alert-title">低库存预警</h3>
          <ul class="alert-list">
            <li v-for="(item, index) in lowStockItems" :key="index">
              <span class="alert-item-name">{{ item.name }}</span>
              <span class="alert-item-detail">当前: {{ item.quantity }}{{ item.unit }} (补货点: {{ item.reorderPoint }}{{ item.unit }})</span>
            </li>
          </ul>
        </div>
        <div v-if="expiringItems.length > 0" class="alert-card">
          <h3 class="alert-title">即将过期预警</h3>
          <ul class="alert-list">
            <li v-for="(item, index) in expiringItems" :key="index">
              <span class="alert-item-name">{{ item.name }}</span>
              <span class="alert-item-detail">批次号: {{ item.batchNumber }} (到期日: {{ item.expirationDate }})</span>
            </li>
          </ul>
        </div>
        <div v-if="lowStockItems.length === 0 && expiringItems.length === 0" class="no-alerts">
          <p>没有库存预警</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import inventoryApi from '../api/inventory';

// 状态变量
const loading = ref(true);
const error = ref(null);

// 库存数据
const inventoryItems = ref([
  { 
    name: '意式浓缩咖啡豆', 
    category: '咖啡', 
    quantity: 150, 
    unit: 'kg', 
    reorderPoint: 20, 
    lastUpdated: '2023-11-15' 
  },
  { 
    name: '牛奶', 
    category: '乳制品', 
    quantity: 50, 
    unit: '升', 
    reorderPoint: 10, 
    lastUpdated: '2023-11-15' 
  },
  { 
    name: '糖', 
    category: '甜味剂', 
    quantity: 100, 
    unit: 'kg', 
    reorderPoint: 15, 
    lastUpdated: '2023-11-15' 
  },
  { 
    name: '巧克力糖浆', 
    category: '糖浆', 
    quantity: 25, 
    unit: '升', 
    reorderPoint: 5, 
    lastUpdated: '2023-11-15' 
  },
  { 
    name: '纸杯', 
    category: '应急物资', 
    quantity: 5000, 
    unit: '件', 
    reorderPoint: 500, 
    lastUpdated: '2023-11-15' 
  }
]);

// 批次管理数据
const batchItems = ref([
  { 
    name: '牛奶', 
    batchNumber: 'B20231110', 
    quantity: 20, 
    expirationDate: '2023-11-20', 
    status: '活跃' 
  },
  { 
    name: '意式浓缩咖啡豆', 
    batchNumber: 'B20231105', 
    quantity: 50, 
    expirationDate: '2024-05-05', 
    status: '活跃' 
  },
  { 
    name: '巧克力糖浆', 
    batchNumber: 'B20231025', 
    quantity: 10, 
    expirationDate: '2024-01-25', 
    status: '活跃' 
  }
]);

// 获取所有数据
async function fetchAllData() {
  loading.value = true;
  error.value = null;
  
  try {
    // 获取库存数据
    const stockData = await inventoryApi.stock.getAll();
    if (stockData && stockData.length > 0) {
      // 转换后端数据格式为前端格式
      inventoryItems.value = stockData.map(item => ({
        id: item.id,
        name: item.product_name || '未命名产品',
        category: item.category_name || '未分类',
        quantity: item.current_quantity || 0,
        unit: item.product_unit || '个',
        reorderPoint: item.minimum_quantity || 0,
        lastUpdated: item.updated_at || '未知'
      }));
    }
    
    // 获取批次数据
    const batchData = await inventoryApi.batches.getAll();
    if (batchData && batchData.length > 0) {
      // 转换后端数据格式为前端格式
      batchItems.value = batchData.map(batch => ({
        id: batch.batch_id,
        name: batch.product_name || '未命名产品',
        batchNumber: batch.batch_no || '未知批次',
        quantity: batch.qty || 0,
        expirationDate: batch.expiry_date || '未知',
        status: getStatusText(batch.status)
      }));
    }
  } catch (err) {
    console.error('获取库存数据失败:', err);
    error.value = '获取数据失败，请稍后重试';
  } finally {
    loading.value = false;
  }
}

// 获取状态文本
function getStatusText(status) {
  const statusMap = {
    'ACTIVE': '活跃',
    'EXPIRED': '已过期',
    'USED_UP': '已用完'
  };
  return statusMap[status] || status;
}

// 格式化日期
function formatDate(dateString) {
  if (!dateString) return '';
  
  const date = new Date(dateString);
  if (isNaN(date.getTime())) return dateString;
  
  return date.toLocaleDateString('zh-CN');
}

// 计算低库存商品
const lowStockItems = computed(() => {
  return inventoryItems.value.filter(item => item.quantity <= item.reorderPoint);
});

// 计算即将过期商品（30天内）
const expiringItems = computed(() => {
  const today = new Date();
  const thirtyDaysLater = new Date();
  thirtyDaysLater.setDate(today.getDate() + 30);
  
  return batchItems.value.filter(item => {
    const expirationDate = new Date(item.expirationDate);
    return expirationDate <= thirtyDaysLater && expirationDate >= today;
  });
});

// 检查是否接近过期（30天内）
function isExpirationNear(dateString) {
  const today = new Date();
  const expirationDate = new Date(dateString);
  const thirtyDaysLater = new Date();
  thirtyDaysLater.setDate(today.getDate() + 30);
  
  return expirationDate <= thirtyDaysLater && expirationDate >= today;
}

// 初始化
onMounted(async () => {
  console.log('库存管理页面已加载');
  try {
    await fetchAllData();
  } catch (err) {
    console.error('初始化数据失败:', err);
    error.value = '初始化数据失败，请刷新页面重试';
    loading.value = false;
  }
});
</script>

<style scoped>
.page-content-container {
  width: 100%;
  background-color: var(--content-bg-color, #FFFFFF);
  border-radius: 12px;
  padding: 0;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  height: 100%;
  display: flex;
  flex-direction: column;
  max-width: 100%;
  overflow-x: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  flex-wrap: wrap;
  gap: 12px;
  width: 100%;
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 1.25em;
  color: var(--primary-text-color, #121714);
  margin: 0;
}

.section-container {
  padding: 0 16px 16px;
  width: 100%;
}

.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 18px;
  line-height: 1.27em;
  color: var(--primary-text-color, #121714);
  margin: 16px 0 8px;
  padding: 0;
}

.table-container {
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
}

.inventory-table, .batch-table {
  width: 100%;
  border-collapse: collapse;
}

.inventory-table th, .inventory-table td,
.batch-table th, .batch-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
}

.inventory-table th, .batch-table th {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.inventory-table td, .batch-table td {
  border-top: 1px solid var(--border-color, #E5E8EB);
  height: 72px;
}

.text-secondary {
  color: var(--secondary-text-color, #638770);
}

.text-warning {
  color: #FF6B6B;
}

.status-badge {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border-radius: 16px;
  padding: 4px 12px;
  font-weight: 500;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
  display: inline-block;
}

.status-badge.inactive {
  background-color: #FFECEC;
  color: #FF6B6B;
}

.alert-container {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 8px;
}

.alert-card {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border-radius: 12px;
  padding: 16px;
  width: calc(50% - 8px);
  min-width: 300px;
  flex: 1;
}

.alert-title {
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 12px 0;
  color: var(--primary-text-color, #121714);
}

.alert-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.alert-list li {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 0;
  border-bottom: 1px solid var(--border-color, #E5E8EB);
}

.alert-list li:last-child {
  border-bottom: none;
}

.alert-item-name {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
}

.alert-item-detail {
  font-size: 14px;
  color: var(--secondary-text-color, #638770);
}

.no-alerts {
  text-align: center;
  padding: 32px;
  color: var(--secondary-text-color, #638770);
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border-radius: 12px;
  width: 100%;
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  width: 100%;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--primary-color, #4CAF50);
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 错误消息 */
.error-message {
  background-color: #FFECEC;
  border-radius: 12px;
  padding: 16px;
  margin: 16px;
  color: #FF6B6B;
  text-align: center;
}

.retry-button {
  background-color: #FF6B6B;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  margin-top: 8px;
  cursor: pointer;
  font-weight: 500;
}

@media (max-width: 768px) {
  .alert-card {
    width: 100%;
  }
}

/* 修复页面宽度超过1024px的问题 */
@media (min-width: 1024px) {
  .page-content-container {
    width: 100%;
    max-width: 100%;
  }
}
</style> 