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
        <h1 class="page-title">{{ order.order_number || '订单详情' }}</h1>
      </div>
      <div class="header-buttons">
        <button v-if="canComplete" class="complete-btn" @click="completeOrder">完成订单</button>
        <button v-if="canCancel" class="cancel-btn" @click="cancelOrder">取消订单</button>
        <button class="print-btn" @click="printOrder">打印订单</button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchOrderData" class="retry-btn">重试</button>
    </div>

    <div v-else class="order-detail-content">
      <!-- 订单基本信息 -->
      <div class="info-card">
        <h2 class="card-title">订单信息</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">订单编号</span>
            <span class="info-value">{{ order.order_number }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">订单类型</span>
            <span class="info-value">{{ getOrderTypeText(order.order_type) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">订单日期</span>
            <span class="info-value">{{ formatDate(order.created_at) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">状态</span>
            <span class="info-value status-badge" :class="getOrderStatusClass(order.status)">
              {{ getOrderStatusText(order.status) }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">小计</span>
            <span class="info-value">¥{{ order.subtotal_amount || '0.00' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">税额</span>
            <span class="info-value">¥{{ order.tax_amount || '0.00' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">总金额</span>
            <span class="info-value">¥{{ order.total_amount || '0.00' }}</span>
          </div>
          <div class="info-item full-width">
            <span class="info-label">备注</span>
            <span class="info-value">{{ order.notes || '-' }}</span>
          </div>
        </div>
      </div>

      <!-- 订单项目列表 -->
      <div class="items-section">
        <div class="section-header">
          <h2 class="section-title">订单项目</h2>
        </div>
        
        <div v-if="loadingItems" class="loading-container">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
        
        <div v-else-if="orderItems.length === 0" class="empty-state">
          <p>暂无订单项目</p>
        </div>
        
        <div v-else class="table-container">
          <table class="items-table">
            <thead>
              <tr>
                <th>商品</th>
                <th>单价</th>
                <th>数量</th>
                <th>小计</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in orderItems" :key="item.id">
                <td>{{ item.product_name }}</td>
                <td>¥{{ item.unit_price }}</td>
                <td>{{ item.quantity }}</td>
                <td>¥{{ calculateSubtotal(item) }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="3" class="total-label">小计</td>
                <td class="total-value">¥{{ order.subtotal_amount || '0.00' }}</td>
              </tr>
              <tr>
                <td colspan="3" class="total-label">税额</td>
                <td class="total-value">¥{{ order.tax_amount || '0.00' }}</td>
              </tr>
              <tr>
                <td colspan="3" class="total-label">总计</td>
                <td class="total-value">¥{{ order.total_amount || '0.00' }}</td>
              </tr>
            </tfoot>
          </table>
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
const orderId = route.params.id;

// 状态变量
const loading = ref(false);
const loadingItems = ref(false);
const error = ref(null);
const order = ref({});
const orderItems = ref([]);

// 获取订单详情
async function fetchOrderData() {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await api.sales.orders.getById(orderId);
    order.value = response;
    console.log('订单详情:', order.value);
    
    // 加载订单项目
    fetchOrderItems();
  } catch (err) {
    console.error('获取订单详情失败:', err);
    error.value = '获取订单详情失败，请稍后重试';
  } finally {
    loading.value = false;
  }
}

// 获取订单项目
async function fetchOrderItems() {
  loadingItems.value = true;
  
  try {
    const response = await api.sales.orderItems.getByOrderId(orderId);
    orderItems.value = response;
    console.log('订单项目:', orderItems.value);
  } catch (err) {
    console.error('获取订单项目失败:', err);
  } finally {
    loadingItems.value = false;
  }
}

// 返回上一页
function goBack() {
  router.back();
}

// 完成订单
async function completeOrder() {
  if (!confirm('确定要将此订单标记为已完成吗？')) {
    return;
  }
  
  try {
    loading.value = true;
    await api.sales.orders.complete(orderId);
    
    // 重新获取订单数据
    fetchOrderData();
    console.log('订单已完成:', orderId);
  } catch (err) {
    console.error('完成订单失败:', err);
    alert('完成订单失败，请稍后重试');
  } finally {
    loading.value = false;
  }
}

// 取消订单
async function cancelOrder() {
  if (!confirm('确定要取消此订单吗？此操作不可逆。')) {
    return;
  }
  
  try {
    loading.value = true;
    await api.sales.orders.cancel(orderId);
    
    // 重新获取订单数据
    fetchOrderData();
    console.log('订单已取消:', orderId);
  } catch (err) {
    console.error('取消订单失败:', err);
    alert('取消订单失败，请稍后重试');
  } finally {
    loading.value = false;
  }
}

// 打印订单
function printOrder() {
  const printContent = createPrintContent();
  const printWindow = window.open('', '_blank');
  printWindow.document.write(printContent);
  printWindow.document.close();
  
  // 延迟一下，确保内容已加载
  setTimeout(() => {
    printWindow.print();
    printWindow.close();
  }, 500);
}

// 创建打印内容
function createPrintContent() {
  const now = new Date();
  const dateStr = now.toLocaleDateString();
  const timeStr = now.toLocaleTimeString();
  
  const header = `
    <h1>咖啡店订单</h1>
    <p>订单号: ${order.value.order_number}</p>
    <p>日期: ${formatDate(order.value.created_at)}</p>
    <p>订单类型: ${getOrderTypeText(order.value.order_type)}</p>
    <hr>
  `;
  
  let items = '<table border="0" width="100%"><tr><th>商品</th><th>数量</th><th>单价</th><th>小计</th></tr>';
  orderItems.value.forEach(item => {
    items += `<tr>
      <td>${item.product_name}</td>
      <td>${item.quantity}</td>
      <td>¥${item.unit_price}</td>
      <td>¥${calculateSubtotal(item)}</td>
    </tr>`;
  });
  items += '</table><hr>';
  
  const summary = `
    <table border="0" width="100%">
      <tr><td>小计:</td><td align="right">¥${order.value.subtotal_amount || '0.00'}</td></tr>
      <tr><td>税额:</td><td align="right">¥${order.value.tax_amount || '0.00'}</td></tr>
      <tr><td><strong>总计:</strong></td><td align="right"><strong>¥${order.value.total_amount || '0.00'}</strong></td></tr>
    </table>
  `;
  
  const footer = `
    <hr>
    <p style="text-align: center">感谢您的惠顾!</p>
  `;
  
  return `
    <!DOCTYPE html>
    <html>
    <head>
      <title>咖啡店订单</title>
      <style>
        body { font-family: Arial, sans-serif; width: 300px; margin: 0 auto; }
        h1 { text-align: center; font-size: 18px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 5px; text-align: left; }
        th { border-bottom: 1px solid #ddd; }
      </style>
    </head>
    <body>
      ${header}
      ${items}
      ${summary}
      ${footer}
    </body>
    </html>
  `;
}

// 计算小计
function calculateSubtotal(item) {
  return (parseFloat(item.unit_price || 0) * parseInt(item.quantity || 0)).toFixed(2);
}

// 格式化日期
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
}

// 订单类型文本转换
function getOrderTypeText(type) {
  const typeMap = {
    'dine-in': '堂食',
    'takeout': '外卖'
  };
  return typeMap[type] || type;
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

// 是否可以完成订单
const canComplete = computed(() => {
  return ['pending', 'processing'].includes(order.value.status);
});

// 是否可以取消订单
const canCancel = computed(() => {
  return ['pending', 'processing'].includes(order.value.status);
});

// 初始化
onMounted(() => {
  console.log('订单详情页面已加载，订单ID:', orderId);
  fetchOrderData();
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

.header-buttons {
  display: flex;
  gap: 12px;
}

.complete-btn, .cancel-btn, .print-btn {
  border: none;
  border-radius: 16px;
  padding: 0 16px;
  height: 32px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 500;
  font-size: 14px;
  line-height: 1.5em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.complete-btn {
  background-color: #E8F5E9;
  color: #388E3C;
}

.cancel-btn {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.print-btn {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  color: var(--primary-text-color, #121714);
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

.order-detail-content {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-card {
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

.info-item.full-width {
  grid-column: 1 / -1;
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

.status-badge {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border-radius: 16px;
  padding: 4px 12px;
  font-weight: 500;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
  display: inline-block;
  width: fit-content;
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

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.items-section {
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

.items-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
  overflow: hidden;
}

.items-table th,
.items-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color, #E5E8EB);
}

.items-table th {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.items-table td {
  font-weight: 400;
  color: var(--primary-text-color, #121714);
}

.items-table tfoot {
  font-weight: 700;
}

.items-table tfoot .total-label {
  text-align: right;
}

.items-table tfoot .total-value {
  color: var(--primary-text-color, #121714);
  font-size: 16px;
}

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .items-table {
    display: block;
    overflow-x: auto;
  }
  
  .items-table th {
    white-space: nowrap;
  }
  
  .header-buttons {
    flex-wrap: wrap;
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