<template>
  <div class="page-content-container">
    <div class="header">
      <h1 class="page-title">采购订单</h1>
      <button class="create-order-btn" @click="createOrder">创建采购订单</button>
    </div>

    <div class="filters">
      <div class="search-bar">
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--secondary-text-color)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <input type="text" placeholder="搜索订单号或供应商" v-model="searchQuery" @input="handleSearch" />
      </div>
      <div class="filter-controls">
        <div class="filter-item">
          <label>状态</label>
          <select v-model="statusFilter" @change="applyFilters">
            <option value="">全部</option>
            <option value="draft">草稿</option>
            <option value="submitted">已提交</option>
            <option value="approved">已批准</option>
            <option value="ordered">已下单</option>
            <option value="partially_received">部分收货</option>
            <option value="fully_received">完全收货</option>
            <option value="cancelled">已取消</option>
            <option value="closed">已关闭</option>
          </select>
        </div>
        <div class="filter-item">
          <label>供应商</label>
          <select v-model="supplierFilter" @change="applyFilters">
            <option value="">全部</option>
            <option v-for="supplier in suppliers" :key="supplier.supplier_id" :value="supplier.supplier_id">
              {{ supplier.name }}
            </option>
          </select>
        </div>
        <div class="filter-item date-range">
          <label>日期范围</label>
          <div class="date-inputs">
            <input type="date" v-model="startDate" @change="applyFilters" />
            <span>至</span>
            <input type="date" v-model="endDate" @change="applyFilters" />
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchOrders" class="retry-btn">重试</button>
    </div>

    <div v-else-if="filteredOrders.length === 0" class="empty-state">
      <p>暂无采购订单</p>
      <button class="create-order-btn" @click="createOrder">创建采购订单</button>
    </div>

    <div v-else class="orders-table-container">
      <table class="orders-table">
        <thead>
          <tr>
            <th>订单编号</th>
            <th>供应商</th>
            <th>订单日期</th>
            <th>预计交货日期</th>
            <th>总金额</th>
            <th>状态</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="order in filteredOrders" :key="order.order_id">
            <td>{{ order.order_number }}</td>
            <td>{{ order.supplier_name }}</td>
            <td>{{ formatDate(order.order_date) }}</td>
            <td>{{ formatDate(order.expected_delivery_date) || '-' }}</td>
            <td>¥{{ order.total_amount }}</td>
            <td>
              <span class="status-badge" :class="getOrderStatusClass(order.status)">
                {{ getOrderStatusText(order.status) }}
              </span>
            </td>
            <td class="actions">
              <span class="action-link" @click="viewOrder(order.order_id)">查看</span>
              <span v-if="order.status === 'draft'" class="action-link" @click="editOrder(order.order_id)">编辑</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/api';

const router = useRouter();

// 状态变量
const loading = ref(false);
const error = ref(null);
const orders = ref([]);
const suppliers = ref([]);
const searchQuery = ref('');
const statusFilter = ref('');
const supplierFilter = ref('');
const startDate = ref('');
const endDate = ref('');

// 获取采购订单列表
async function fetchOrders() {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await api.purchase.orders.getAll();
    orders.value = response;
    console.log('获取到采购订单数据:', response);
  } catch (err) {
    console.error('获取采购订单列表失败:', err);
    error.value = '获取采购订单列表失败，请稍后重试';
  } finally {
    loading.value = false;
  }
}

// 获取供应商列表（用于筛选）
async function fetchSuppliers() {
  try {
    const response = await api.purchase.suppliers.getAll();
    suppliers.value = response;
    console.log('获取到供应商数据:', response);
  } catch (err) {
    console.error('获取供应商列表失败:', err);
  }
}

// 过滤订单
const filteredOrders = computed(() => {
  let result = orders.value;
  
  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(order => 
      (order.order_number && order.order_number.toLowerCase().includes(query)) ||
      (order.supplier_name && order.supplier_name.toLowerCase().includes(query))
    );
  }
  
  // 状态过滤
  if (statusFilter.value) {
    result = result.filter(order => order.status === statusFilter.value);
  }
  
  // 供应商过滤
  if (supplierFilter.value) {
    result = result.filter(order => order.supplier === parseInt(supplierFilter.value));
  }
  
  // 日期范围过滤
  if (startDate.value) {
    const start = new Date(startDate.value);
    result = result.filter(order => new Date(order.order_date) >= start);
  }
  
  if (endDate.value) {
    const end = new Date(endDate.value);
    end.setHours(23, 59, 59, 999); // 设置为当天结束
    result = result.filter(order => new Date(order.order_date) <= end);
  }
  
  return result;
});

// 搜索处理
function handleSearch() {
  console.log('搜索:', searchQuery.value);
}

// 应用过滤器
function applyFilters() {
  console.log('应用过滤器:', {
    status: statusFilter.value,
    supplier: supplierFilter.value,
    startDate: startDate.value,
    endDate: endDate.value
  });
}

// 创建采购订单
function createOrder() {
  router.push({ name: 'purchase-order-create' });
}

// 查看订单详情
function viewOrder(orderId) {
  router.push(`/procurement/orders/${orderId}`);
}

// 编辑订单
function editOrder(orderId) {
  router.push({
    name: 'purchase-order-detail',
    params: { id: orderId },
    query: { edit: true }
  });
}

// 订单状态文本转换
function getOrderStatusText(status) {
  const statusMap = {
    'draft': '草稿',
    'submitted': '已提交',
    'approved': '已批准',
    'rejected': '已拒绝',
    'ordered': '已下单',
    'partially_received': '部分收货',
    'fully_received': '完全收货',
    'cancelled': '已取消',
    'closed': '已关闭'
  };
  return statusMap[status] || status;
}

// 订单状态样式
function getOrderStatusClass(status) {
  const classMap = {
    'draft': 'draft',
    'submitted': 'submitted',
    'approved': 'approved',
    'rejected': 'rejected',
    'ordered': 'ordered',
    'partially_received': 'partial',
    'fully_received': 'complete',
    'cancelled': 'cancelled',
    'closed': 'closed'
  };
  return classMap[status] || '';
}

// 格式化日期
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN');
}

// 初始化
onMounted(async () => {
  console.log('采购订单列表页面已加载');
  await Promise.all([fetchOrders(), fetchSuppliers()]);
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

.create-order-btn {
  background-color: var(--primary-text-color, #121714);
  border: none;
  border-radius: 16px;
  padding: 0 16px;
  height: 32px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 500;
  font-size: 14px;
  line-height: 1.5em;
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.filters {
  padding: 0 16px 16px;
  border-bottom: 1px solid var(--border-color, #DBE5DE);
}

.search-bar {
  display: flex;
  align-items: center;
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border-radius: 12px;
  height: 48px;
  padding: 0 16px;
  width: 100%;
  margin-bottom: 16px;
}

.search-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
}

.search-bar input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  color: var(--primary-text-color, #121714);
  outline: none;
  width: 100%;
}

.search-bar input::placeholder {
  color: var(--secondary-text-color, #638770);
}

.filter-controls {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}

.filter-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-item label {
  font-size: 14px;
  color: var(--secondary-text-color, #638770);
}

.filter-item select,
.filter-item input {
  padding: 8px 12px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 8px;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.date-range {
  flex-grow: 1;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-inputs input {
  flex: 1;
}

.loading-container, .error-container, .empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  width: 100%;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--secondary-text-color, #638770);
  width: 30px;
  height: 30px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.retry-btn {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  margin-top: 16px;
  cursor: pointer;
}

.empty-state {
  color: var(--secondary-text-color, #638770);
  text-align: center;
}

.empty-state p {
  margin-bottom: 16px;
}

.orders-table-container {
  padding: 16px;
  width: 100%;
  overflow-x: auto;
}

.orders-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
  overflow: hidden;
}

.orders-table th,
.orders-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color, #E5E8EB);
}

.orders-table th {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.orders-table td {
  font-weight: 400;
  color: var(--primary-text-color, #121714);
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

/* 订单状态样式 */
.status-badge.draft {
  background-color: #E0E0E0;
  color: #616161;
}

.status-badge.submitted {
  background-color: #E3F2FD;
  color: #1976D2;
}

.status-badge.approved {
  background-color: #E8F5E9;
  color: #388E3C;
}

.status-badge.rejected {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.status-badge.ordered {
  background-color: #FFF8E1;
  color: #FFA000;
}

.status-badge.partial {
  background-color: #F3E5F5;
  color: #7B1FA2;
}

.status-badge.complete {
  background-color: #E8F5E9;
  color: #388E3C;
}

.status-badge.cancelled {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.status-badge.closed {
  background-color: #ECEFF1;
  color: #455A64;
}

.actions {
  white-space: nowrap;
}

.action-link {
  color: var(--secondary-text-color, #638770);
  font-weight: 700;
  cursor: pointer;
  margin-right: 12px;
}

@media (max-width: 768px) {
  .filter-controls {
    flex-direction: column;
  }
  
  .date-range {
    width: 100%;
  }
  
  .orders-table {
    display: block;
    overflow-x: auto;
  }
  
  .orders-table th {
    white-space: nowrap;
  }
}
</style> 