<template>
  <div class="page-content-container">
    <div class="header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="19" y1="12" x2="5" y2="12"></line>
            <polyline points="12 19 5 12 12 5"></polyline>
          </svg>
          返回
        </button>
        <h1 class="page-title">{{ customer.name || '客户' }}的订单</h1>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchData" class="retry-btn">重试</button>
    </div>

    <div v-else class="customer-detail-content">
      <!-- 客户基本信息 -->
      <div class="info-card">
        <h2 class="card-title">客户信息</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">姓名</span>
            <span class="info-value">{{ customer.name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">电话</span>
            <span class="info-value">{{ customer.phone }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">邮箱</span>
            <span class="info-value">{{ customer.email || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">会员等级</span>
            <span class="info-value">{{ getMembershipLevelText(customer.membership_level) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">积分</span>
            <span class="info-value">{{ customer.points || 0 }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">注册日期</span>
            <span class="info-value">{{ formatDate(customer.created_at) }}</span>
          </div>
        </div>
      </div>

      <!-- 订单列表 -->
      <div class="orders-section">
        <div class="section-header">
          <h2 class="section-title">订单历史</h2>
        </div>
        
        <div v-if="orders.length === 0" class="empty-state">
          <p>该客户暂无订单记录</p>
        </div>
        
        <div v-else class="table-container">
          <table class="orders-table">
            <thead>
              <tr>
                <th>订单号</th>
                <th>日期</th>
                <th>金额</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in orders" :key="order.order_id">
                <td>{{ order.order_number }}</td>
                <td>{{ formatDate(order.created_at) }}</td>
                <td>¥{{ order.total_amount }}</td>
                <td>
                  <span class="status-badge" :class="getOrderStatusClass(order.status)">
                    {{ getOrderStatusText(order.status) }}
                  </span>
                </td>
                <td class="actions">
                  <span class="action-link" @click="viewOrder(order.order_id)">查看</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 消费统计 -->
      <div class="stats-card">
        <h2 class="card-title">消费统计</h2>
        <div class="stats-grid">
          <div class="stat-item">
            <span class="stat-label">订单总数</span>
            <span class="stat-value">{{ orders.length }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">总消费金额</span>
            <span class="stat-value">¥{{ calculateTotalSpent() }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">平均订单金额</span>
            <span class="stat-value">¥{{ calculateAverageOrderValue() }}</span>
          </div>
          <div class="stat-item">
            <span class="stat-label">最近消费</span>
            <span class="stat-value">{{ getLastOrderDate() }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '../api/api';

const router = useRouter();
const route = useRoute();
const customerId = route.params.id;

// 状态变量
const loading = ref(false);
const error = ref(null);
const customer = ref({});
const orders = ref([]);

// 获取客户数据和订单
async function fetchData() {
  loading.value = true;
  error.value = null;
  
  try {
    // 获取客户信息
    const customerResponse = await api.sales.customers.getById(customerId);
    customer.value = customerResponse;
    console.log('获取到客户数据:', customer.value);
    
    // 获取客户订单
    const ordersResponse = await api.sales.orders.getByCustomerId(customerId);
    orders.value = ordersResponse;
    console.log('获取到客户订单:', orders.value);
  } catch (err) {
    console.error('获取数据失败:', err);
    error.value = '获取数据失败，请稍后重试';
  } finally {
    loading.value = false;
  }
}

// 返回上一页
function goBack() {
  router.back();
}

// 查看订单详情
function viewOrder(orderId) {
  router.push(`/orders/${orderId}`);
}

// 计算总消费金额
function calculateTotalSpent() {
  const total = orders.value.reduce((sum, order) => sum + parseFloat(order.total_amount || 0), 0);
  return total.toFixed(2);
}

// 计算平均订单金额
function calculateAverageOrderValue() {
  if (orders.value.length === 0) return '0.00';
  const total = orders.value.reduce((sum, order) => sum + parseFloat(order.total_amount || 0), 0);
  return (total / orders.value.length).toFixed(2);
}

// 获取最近消费日期
function getLastOrderDate() {
  if (orders.value.length === 0) return '无';
  
  const dates = orders.value
    .map(order => new Date(order.created_at))
    .sort((a, b) => b - a);
  
  return formatDate(dates[0]);
}

// 会员等级文本转换
function getMembershipLevelText(level) {
  const levelMap = {
    'regular': '普通会员',
    'silver': '银卡会员',
    'gold': '金卡会员',
    'platinum': '白金会员'
  };
  return levelMap[level] || level;
}

// 订单状态文本转换
function getOrderStatusText(status) {
  const statusMap = {
    'pending': '待处理',
    'processing': '处理中',
    'completed': '已完成',
    'cancelled': '已取消'
  };
  return statusMap[status] || status;
}

// 订单状态样式
function getOrderStatusClass(status) {
  const classMap = {
    'pending': 'pending',
    'processing': 'processing',
    'completed': 'completed',
    'cancelled': 'cancelled'
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
onMounted(() => {
  console.log('客户订单页面已加载，客户ID:', customerId);
  fetchData();
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
  border-bottom: 1px solid var(--border-color, #DBE5DE);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  color: var(--secondary-text-color, #638770);
  cursor: pointer;
  font-weight: 500;
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 28px;
  line-height: 1.25em;
  color: var(--primary-text-color, #121714);
  margin: 0;
}

.loading-container, .error-container {
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

.customer-detail-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-card, .stats-card {
  background-color: var(--content-bg-color, #FFFFFF);
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
  padding: 24px;
}

.card-title, .section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 18px;
  margin: 0 0 16px 0;
  color: var(--primary-text-color, #121714);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 14px;
  color: var(--secondary-text-color, #638770);
}

.info-value {
  font-size: 16px;
  color: var(--primary-text-color, #121714);
  font-weight: 500;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.orders-section {
  display: flex;
  flex-direction: column;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  text-align: center;
  color: var(--secondary-text-color, #638770);
}

.table-container {
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
.status-badge.pending {
  background-color: #FFF8E1;
  color: #FFA000;
}

.status-badge.processing {
  background-color: #E3F2FD;
  color: #1976D2;
}

.status-badge.completed {
  background-color: #E8F5E9;
  color: #388E3C;
}

.status-badge.cancelled {
  background-color: #FFEBEE;
  color: #D32F2F;
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

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border-radius: 12px;
  padding: 16px;
}

.stat-label {
  font-size: 14px;
  color: var(--secondary-text-color, #638770);
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-text-color, #121714);
}

@media (max-width: 768px) {
  .info-grid, .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .orders-table {
    display: block;
    overflow-x: auto;
  }
  
  .orders-table th {
    white-space: nowrap;
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