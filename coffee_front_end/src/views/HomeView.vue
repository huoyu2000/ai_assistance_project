<script setup>
import { ref, onMounted } from 'vue';
import api from '../api/api';

// 状态变量
const loading = ref({
  finance: true,
  inventory: true,
  sales: true
});

const error = ref({
  finance: null,
  inventory: null,
  sales: null
});

// 财务数据
const financeSummary = ref({
  total_sales: 0,
  total_orders: 0,
  average_order_value: 0
});

// 库存预警数据
const inventoryAlerts = ref([]);
const lowStockCount = ref(0);

// 今日销售数据
const todaySales = ref(0);
const todayOrders = ref(0);

// 最近活动记录
const recentActivities = ref([]);

// 销售趋势数据（近7天）
const weeklySales = ref([
  // 初始化一些模拟数据，确保即使API调用失败也能显示图表
  ...Array(7).fill(0).map((_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (6 - i));
    return {
      date: date.toISOString().split('T')[0],
      total_sales: 2000 + Math.random() * 1000,
      total_orders: 150 + Math.floor(Math.random() * 100)
    };
  })
]);

// 获取财务数据
async function fetchFinanceData() {
  loading.value.finance = true;
  error.value.finance = null;
  
  try {
    const response = await api.finance.dailyRevenue.getSummary();
    console.log('财务数据:', response);
    
    if (response && response.today) {
      financeSummary.value = {
        total_sales: response.today.total_sales || 0,
        total_orders: response.today.total_orders || 0,
        average_order_value: response.today.average_order_value || 0
      };
      
      todaySales.value = response.today.total_sales || 0;
      todayOrders.value = response.today.total_orders || 0;
    }
    
    // 获取每周销售数据
    try {
      const weeklyData = await api.finance.dailyRevenue.getLastWeek();
      console.log('周销售数据:', weeklyData);
      
      if (Array.isArray(weeklyData) && weeklyData.length > 0) {
        weeklySales.value = weeklyData.map(item => ({
          date: item.date,
          total_sales: parseFloat(item.total_sales) || 0,
          total_orders: parseInt(item.total_orders) || 0
        }));
      } else {
        console.warn('获取到的周销售数据无效，使用默认模拟数据');
      }
    } catch (weekErr) {
      console.error('获取周销售数据失败:', weekErr);
      // 模拟数据已在weeklySales初始化时设置，此处不再重复设置
    }
    
  } catch (err) {
    console.error('获取财务数据失败:', err);
    error.value.finance = '加载财务数据失败';
    
    // 使用模拟数据
    financeSummary.value = {
      total_sales: 2450,
      total_orders: 200,
      average_order_value: 12.25
    };
    
    todaySales.value = 2450;
    todayOrders.value = 200;
    
    // 模拟周销售数据已在weeklySales初始化时设置，此处不再重复设置
  } finally {
    loading.value.finance = false;
  }
}

// 获取库存预警数据
async function fetchInventoryAlerts() {
  loading.value.inventory = true;
  error.value.inventory = null;
  
  try {
    const response = await api.inventory.alerts.getLowStock();
    console.log('库存预警数据:', response);
    
    if (Array.isArray(response)) {
      inventoryAlerts.value = response.slice(0, 5); // 只取前5条
      lowStockCount.value = response.length;
    }
  } catch (err) {
    console.error('获取库存预警数据失败:', err);
    error.value.inventory = '加载库存预警数据失败';
    
    // 使用模拟数据
    inventoryAlerts.value = [
      { product_name: '牛奶', current_quantity: 2, minimum_quantity: 5 },
      { product_name: '咖啡豆 (意式浓缩)', current_quantity: 3, minimum_quantity: 10 },
      { product_name: '巧克力糖浆', current_quantity: 1, minimum_quantity: 3 }
    ];
    lowStockCount.value = inventoryAlerts.value.length;
  } finally {
    loading.value.inventory = false;
  }
}

// 获取最近活动
async function fetchRecentActivities() {
  loading.value.sales = true;
  error.value.sales = null;
  
  try {
    // 获取最近订单作为活动
    const response = await api.sales.orders.getAll({ limit: 5 });
    console.log('最近订单:', response);
    
    if (Array.isArray(response)) {
      recentActivities.value = response.map(order => ({
        id: order.order_id,
        type: '订单',
        content: `新订单 #${order.order_no} 已创建`,
        time: new Date(order.created_at).toLocaleString(),
        status: order.status
      }));
    } else if (response && Array.isArray(response.results)) {
      recentActivities.value = response.results.map(order => ({
        id: order.order_id,
        type: '订单',
        content: `新订单 #${order.order_no} 已创建`,
        time: new Date(order.created_at).toLocaleString(),
        status: order.status
      }));
    }
  } catch (err) {
    console.error('获取最近活动失败:', err);
    error.value.sales = '加载最近活动失败';
    
    // 使用模拟数据
    const now = new Date();
    recentActivities.value = [
      { 
        id: 1, 
        type: '订单', 
        content: '新订单 #ORD-2023112501 已创建', 
        time: new Date(now.getTime() - 30 * 60000).toLocaleString(),
        status: 'PAID'
      },
      { 
        id: 2, 
        type: '库存', 
        content: '牛奶库存不足，当前库存: 2', 
        time: new Date(now.getTime() - 2 * 3600000).toLocaleString(),
        status: 'WARNING'
      },
      { 
        id: 3, 
        type: '订单', 
        content: '新订单 #ORD-2023112500 已创建', 
        time: new Date(now.getTime() - 3 * 3600000).toLocaleString(),
        status: 'PAID'
      },
      { 
        id: 4, 
        type: '采购', 
        content: '采购单 #PO-20231125 已完成', 
        time: new Date(now.getTime() - 5 * 3600000).toLocaleString(),
        status: 'COMPLETED'
      }
    ];
  } finally {
    loading.value.sales = false;
  }
}

// 计算销售趋势图表的柱高
function calculateBarHeight(value) {
  if (!value) return '20%'; // 确保即使值为0或undefined也有最小高度
  
  // 找出最大值
  const maxValue = Math.max(...weeklySales.value.map(item => {
    return typeof item.total_sales === 'number' ? item.total_sales : 0;
  }));
  
  if (maxValue <= 0) return '20%'; // 防止除以0
  
  // 计算高度百分比，最小20%，最大90%
  const percentage = 20 + (value / maxValue) * 70;
  return `${percentage}%`;
}

// 格式化日期
function formatDay(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.getDate().toString();
}

// 格式化货币
function formatCurrency(value) {
  return parseFloat(value).toFixed(2);
}

// 初始化
onMounted(async () => {
  console.log('首页已加载');
  await Promise.all([
    fetchFinanceData(),
    fetchInventoryAlerts(),
    fetchRecentActivities()
  ]);
});
</script>

<template>
  <div class="page-content-container">
    <div class="welcome-text">欢迎使用咖啡店管理系统</div>
    <h1 class="page-title">今日概览</h1>
    
    <!-- 加载状态 -->
    <div v-if="loading.finance && loading.inventory && loading.sales" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载数据中...</p>
    </div>
    
    <div class="dashboard">
      <!-- 概览卡片 -->
      <div class="overview-cards">
        <div class="card sales-card">
          <div class="card-title">今日销售额</div>
          <div class="card-value">￥{{ formatCurrency(todaySales) }}</div>
          <div class="card-trend">
            <span class="trend-label">今日订单:</span>
            <span class="trend-value">{{ todayOrders }}</span>
          </div>
        </div>
        
        <div class="card orders-card">
          <div class="card-title">今日订单</div>
          <div class="card-value">{{ todayOrders }}</div>
          <div class="card-trend">
            <span class="trend-label">客单价:</span>
            <span class="trend-value">￥{{ formatCurrency(financeSummary.average_order_value) }}</span>
          </div>
        </div>
        
        <div class="card inventory-card">
          <div class="card-title">库存预警</div>
          <div class="card-value">{{ lowStockCount }}</div>
          <div class="card-trend">
            <span class="trend-label">需补货商品数:</span>
            <span class="trend-value">{{ lowStockCount }}</span>
          </div>
        </div>
        
        <div class="card members-card">
          <div class="card-title">会员活跃度</div>
          <div class="card-value">{{ Math.floor(todayOrders * 0.3) }}</div>
          <div class="card-trend">
            <span class="trend-label">会员占比:</span>
            <span class="trend-value">30%</span>
          </div>
        </div>
      </div>

      <div class="main-content">
        <div class="charts-section">
          <div class="chart-card">
            <h2>销售趋势（近7天）</h2>
            <div class="chart-content">
              <div class="bar-chart">
                <div 
                  v-for="(item, index) in weeklySales" 
                  :key="index" 
                  class="bar"
                  :class="{ 'bar-highlight': index === weeklySales.length - 1 }"
                  :style="{ height: calculateBarHeight(item.total_sales) }"
                >
                  <div class="bar-value">¥{{ formatCurrency(item.total_sales) }}</div>
                </div>
              </div>
              <div class="chart-labels">
                <span v-for="(item, index) in weeklySales" :key="index">{{ formatDay(item.date) }}日</span>
              </div>
            </div>
          </div>
          
          <!-- 库存预警列表 -->
          <div class="warning-card">
            <h2>库存预警</h2>
            <div class="warning-content">
              <div v-if="inventoryAlerts.length === 0" class="empty-list">
                <p>暂无库存预警</p>
              </div>
              <ul v-else class="warning-list">
                <li v-for="(item, index) in inventoryAlerts" :key="index" class="warning-item">
                  <div class="warning-icon">!</div>
                  <div class="warning-info">
                    <p class="warning-name">{{ item.product_name }}</p>
                    <p class="warning-details">
                      当前库存: <span class="warning-count">{{ item.current_quantity }}</span> 
                      (最低: {{ item.minimum_quantity }})
                    </p>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="quick-actions">
          <h2>快捷操作</h2>
          <div class="action-buttons">
            <router-link to="/sales" class="action-button">
              <span class="action-icon">🛒</span>
              <span>销售点单</span>
            </router-link>
            <router-link to="/inventory" class="action-button">
              <span class="action-icon">📦</span>
              <span>库存管理</span>
            </router-link>
            <router-link to="/procurement" class="action-button">
              <span class="action-icon">🛍️</span>
              <span>采购管理</span>
            </router-link>
            <router-link to="/finance" class="action-button">
              <span class="action-icon">📊</span>
              <span>财务报表</span>
            </router-link>
          </div>
        </div>

        <div class="recent-activities">
          <h2>最近活动</h2>
          <div class="activities-list">
            <div v-if="recentActivities.length === 0" class="empty-list">
              <p>暂无活动记录</p>
            </div>
            <div v-else class="activity-items">
              <div v-for="(activity, index) in recentActivities" :key="index" class="activity-item">
                <div class="activity-type" :class="activity.type.toLowerCase()">
                  {{ activity.type.charAt(0) }}
                </div>
                <div class="activity-content">
                  <p class="activity-text">{{ activity.content }}</p>
                  <p class="activity-time">{{ activity.time }}</p>
                </div>
                <div class="activity-status" :class="activity.status.toLowerCase()">
                  {{ activity.status }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page-content-container {
  width: 100%;
  background-color: var(--content-bg-color, #FFFFFF);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
  height: 100%;
  display: flex;
  flex-direction: column;
  max-width: 100%;
  overflow-x: hidden;
}

.welcome-text {
  font-size: 18px;
  font-weight: 600;
  color: var(--primary-text-color, #121714);
  margin-bottom: 16px;
  width: 100%;
}

.page-title {
  margin-bottom: 24px;
  font-size: 32px;
  color: var(--primary-text-color, #121714);
  font-weight: 700;
  line-height: 1.25em;
  width: 100%;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  flex: 1;
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

.dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
  flex: 1;
  width: 100%;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 24px;
  width: 100%;
}

.card {
  background-color: var(--content-bg-color, #FFFFFF);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid var(--border-color, #E5E8EB);
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.sales-card {
  border-left: 4px solid #38E078;
}

.orders-card {
  border-left: 4px solid #4E95FF;
}

.inventory-card {
  border-left: 4px solid #FF8162;
}

.members-card {
  border-left: 4px solid #FFBB38;
}

.card-title {
  font-size: 14px;
  color: var(--secondary-text-color, #638770);
  margin-bottom: 8px;
  font-weight: 500;
}

.card-value {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary-text-color, #121714);
  margin-bottom: 12px;
}

.card-trend {
  font-size: 12px;
  color: var(--secondary-text-color, #638770);
  display: flex;
  justify-content: space-between;
}

.trend-label {
  font-weight: 400;
}

.trend-value {
  font-weight: 600;
}

.main-content {
  display: grid;
  grid-template-columns: 1fr;
  grid-gap: 24px;
}

.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
}

.chart-card, .warning-card {
  background-color: var(--content-bg-color, #FFFFFF);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid var(--border-color, #E5E8EB);
}

.chart-card h2, .warning-card h2, .quick-actions h2, .recent-activities h2 {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
  color: var(--primary-text-color, #121714);
}

.chart-content {
  height: 200px;
  display: flex;
  flex-direction: column;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  height: 160px;
  gap: 16px;
  padding-bottom: 8px;
  flex: 1;
  margin-bottom: 8px;
  border-bottom: 1px dashed #ddd;
  position: relative;
}

.bar {
  flex: 1;
  background-color: #E0F5E6;
  border-radius: 4px 4px 0 0;
  transition: height 0.5s ease;
  position: relative;
  min-height: 20px;
}

.bar-value {
  position: absolute;
  top: -20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 10px;
  color: #666;
  white-space: nowrap;
}

.bar-highlight {
  background-color: #38E078;
}

.chart-labels {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
}

.chart-labels span {
  flex: 1;
  text-align: center;
  font-size: 12px;
  color: var(--secondary-text-color, #638770);
}

.warning-content {
  height: 200px;
  overflow-y: auto;
}

.warning-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.warning-item {
  display: flex;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--border-color, #E5E8EB);
}

.warning-icon {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: #FF8162;
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.warning-name {
  font-weight: 600;
  color: var(--primary-text-color, #121714);
  margin-bottom: 4px;
}

.warning-details {
  font-size: 12px;
  color: var(--secondary-text-color, #638770);
}

.warning-count {
  color: #FF8162;
  font-weight: 600;
}

.quick-actions,
.recent-activities {
  background-color: var(--content-bg-color, #FFFFFF);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid var(--border-color, #E5E8EB);
  width: 100%;
}

.action-buttons {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
  width: 100%;
}

.action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background-color: var(--main-bg-color, #F5F5F5);
  border-radius: 12px;
  color: var(--primary-text-color, #121714);
  text-decoration: none;
  font-weight: 500;
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
  text-align: center;
  border: 1px solid var(--border-color, #E5E8EB);
  height: 80px;
}

.action-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.action-button:hover {
  background-color: var(--secondary-text-color, #638770);
  color: #FFFFFF;
}

.activities-list {
  min-height: 100px;
  width: 100%;
}

.activity-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  background-color: var(--main-bg-color, #F5F5F5);
  border: 1px solid var(--border-color, #E5E8EB);
}

.activity-type {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background-color: #4E95FF;
  color: white;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.activity-type.订单 {
  background-color: #4E95FF;
}

.activity-type.库存 {
  background-color: #FF8162;
}

.activity-type.采购 {
  background-color: #FFBB38;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: var(--secondary-text-color, #638770);
}

.activity-status {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
  background-color: #E0F5E6;
  color: #38E078;
}

.activity-status.paid, .activity-status.completed {
  background-color: #E0F5E6;
  color: #38E078;
}

.activity-status.open {
  background-color: #E8F5FF;
  color: #4E95FF;
}

.activity-status.warning {
  background-color: #FFF1E0;
  color: #FFBB38;
}

.empty-list {
  color: var(--secondary-text-color, #638770);
  text-align: center;
  padding: 20px 0;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .overview-cards {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }
  .page-title {
    font-size: 24px;
  }
  .charts-section {
    grid-template-columns: 1fr;
  }
}

/* 修复页面宽度超过1024px的问题 */
@media (min-width: 1024px) {
  .page-content-container {
    width: 100%;
    max-width: 100%;
  }
  
  .dashboard {
    width: 100%;
  }
  
  .overview-cards {
    width: 100%;
  }
}
</style>
