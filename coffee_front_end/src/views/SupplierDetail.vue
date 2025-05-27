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
        <h1 class="page-title">{{ supplier.name || '供应商详情' }}</h1>
      </div>
      <div class="header-buttons">
        <button class="edit-btn" @click="editSupplier">编辑</button>
        <button class="create-order-btn" @click="createOrder">创建采购订单</button>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchSupplierData" class="retry-btn">重试</button>
    </div>

    <div v-else class="supplier-detail-content">
      <div class="info-card">
        <h2 class="card-title">基本信息</h2>
        <div class="info-grid">
          <div class="info-item">
            <span class="info-label">供应商名称</span>
            <span class="info-value">{{ supplier.name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">类别</span>
            <span class="info-value">{{ supplier.category || '未分类' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">联系人</span>
            <span class="info-value">{{ supplier.contact_name || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">电话</span>
            <span class="info-value">{{ supplier.phone || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">邮箱</span>
            <span class="info-value">{{ supplier.email || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">地址</span>
            <span class="info-value">{{ supplier.address || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">状态</span>
            <span class="info-value status-badge" :class="{ 'inactive': supplier.status === 'INACTIVE' }">
              {{ getStatusText(supplier.status) }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">创建时间</span>
            <span class="info-value">{{ formatDate(supplier.created_at) }}</span>
          </div>
        </div>
      </div>

      <div class="tabs">
        <div 
          v-for="(tab, index) in tabs" 
          :key="index" 
          class="tab" 
          :class="{ active: activeTab === tab.id }"
          @click="activeTab = tab.id"
        >
          {{ tab.name }}
        </div>
      </div>

      <!-- 供应商产品列表 -->
      <div v-if="activeTab === 'products'" class="tab-content">
        <div class="tab-header">
          <h2 class="tab-title">供应商产品</h2>
          <button class="add-btn" @click="addProduct">添加产品</button>
        </div>
        <div v-if="loadingProducts" class="loading-container">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
        <div v-else-if="supplierProducts.length === 0" class="empty-state">
          <p>该供应商暂无产品信息</p>
          <button class="add-btn" @click="addProduct">添加产品</button>
        </div>
        <div v-else class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>产品名称</th>
                <th>供应商编码</th>
                <th>单位</th>
                <th>价格</th>
                <th>最小订购量</th>
                <th>交货周期(天)</th>
                <th>首选供应商</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="product in supplierProducts" :key="product.id">
                <td>{{ product.product_name }}</td>
                <td>{{ product.supplier_product_code || '-' }}</td>
                <td>{{ product.product_unit }}</td>
                <td>¥{{ product.price }}</td>
                <td>{{ product.min_order_quantity }} {{ product.product_unit }}</td>
                <td>{{ product.lead_time_days }}</td>
                <td>
                  <span class="badge" :class="{ 'active': product.is_preferred }">
                    {{ product.is_preferred ? '是' : '否' }}
                  </span>
                </td>
                <td>
                  <span class="action-link" @click="editProduct(product)">编辑</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 采购订单历史 -->
      <div v-if="activeTab === 'orders'" class="tab-content">
        <div class="tab-header">
          <h2 class="tab-title">采购订单历史</h2>
          <button class="add-btn" @click="createOrder">创建采购订单</button>
        </div>
        <div v-if="loadingOrders" class="loading-container">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
        <div v-else-if="purchaseOrders.length === 0" class="empty-state">
          <p>该供应商暂无采购订单</p>
          <button class="add-btn" @click="createOrder">创建采购订单</button>
        </div>
        <div v-else class="table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>订单编号</th>
                <th>订单日期</th>
                <th>预计交货日期</th>
                <th>总金额</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in purchaseOrders" :key="order.order_id">
                <td>{{ order.order_number }}</td>
                <td>{{ formatDate(order.order_date) }}</td>
                <td>{{ formatDate(order.expected_delivery_date) || '-' }}</td>
                <td>¥{{ order.total_amount }}</td>
                <td>
                  <span class="status-badge" :class="getOrderStatusClass(order.status)">
                    {{ getOrderStatusText(order.status) }}
                  </span>
                </td>
                <td>
                  <span class="action-link" @click="viewOrder(order.order_id)">查看</span>
                </td>
              </tr>
            </tbody>
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
const supplierId = route.params.id;

// 状态变量
const loading = ref(false);
const loadingProducts = ref(false);
const loadingOrders = ref(false);
const error = ref(null);
const supplier = ref({});
const supplierProducts = ref([]);
const purchaseOrders = ref([]);

// 选项卡
const tabs = [
  { id: 'products', name: '供应商产品' },
  { id: 'orders', name: '采购订单历史' }
];
const activeTab = ref('products');

// 获取供应商详情
async function fetchSupplierData() {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await api.purchase.suppliers.getById(supplierId);
    supplier.value = response;
    console.log('供应商详情:', supplier.value);
    
    // 加载供应商产品
    fetchSupplierProducts();
    
    // 加载采购订单
    fetchPurchaseOrders();
  } catch (err) {
    console.error('获取供应商详情失败:', err);
    error.value = '获取供应商详情失败，请稍后重试';
  } finally {
    loading.value = false;
  }
}

// 获取供应商产品
async function fetchSupplierProducts() {
  loadingProducts.value = true;
  
  try {
    const response = await api.purchase.suppliers.getProducts(supplierId);
    supplierProducts.value = response;
    console.log('供应商产品:', supplierProducts.value);
  } catch (err) {
    console.error('获取供应商产品失败:', err);
  } finally {
    loadingProducts.value = false;
  }
}

// 获取采购订单
async function fetchPurchaseOrders() {
  loadingOrders.value = true;
  
  try {
    const response = await api.purchase.orders.getAll({ supplier: supplierId });
    purchaseOrders.value = response;
    console.log('采购订单:', purchaseOrders.value);
  } catch (err) {
    console.error('获取采购订单失败:', err);
  } finally {
    loadingOrders.value = false;
  }
}

// 返回上一页
function goBack() {
  router.back();
}

// 编辑供应商
function editSupplier() {
  // 跳转到编辑页面或打开编辑模态框
  console.log('编辑供应商:', supplier.value);
}

// 创建采购订单
function createOrder() {
  router.push({
    name: 'purchase-order-create',
    query: { supplier: supplierId }
  });
}

// 添加产品
function addProduct() {
  // 打开添加产品模态框
  console.log('添加产品给供应商:', supplier.value);
}

// 编辑产品
function editProduct(product) {
  // 打开编辑产品模态框
  console.log('编辑供应商产品:', product);
}

// 查看订单
function viewOrder(orderId) {
  router.push(`/procurement/orders/${orderId}`);
}

// 状态文本转换
function getStatusText(status) {
  const statusMap = {
    'ACTIVE': '活跃',
    'INACTIVE': '停用'
  };
  return statusMap[status] || status;
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
onMounted(() => {
  console.log('供应商详情页面已加载，供应商ID:', supplierId);
  fetchSupplierData();
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

.edit-btn, .create-order-btn, .add-btn {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border: none;
  border-radius: 16px;
  padding: 0 16px;
  height: 32px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 500;
  font-size: 14px;
  line-height: 1.5em;
  color: var(--primary-text-color, #121714);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.create-order-btn {
  background-color: var(--primary-text-color, #121714);
  color: white;
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

.supplier-detail-content {
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

.card-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 18px;
  margin: 0 0 16px 0;
  color: var(--primary-text-color, #121714);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
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

.status-badge.inactive {
  background-color: #FFE0E0;
  color: #E53935;
}

.tabs {
  display: flex;
  gap: 32px;
  border-bottom: 1px solid var(--border-color, #DBE5DE);
}

.tab {
  padding: 16px 0 13px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 14px;
  line-height: 1.5em;
  color: var(--secondary-text-color, #638770);
  cursor: pointer;
  position: relative;
  border-bottom: 3px solid transparent;
}

.tab.active {
  color: var(--primary-text-color, #121714);
  border-bottom-color: var(--primary-text-color, #121714);
}

.tab-content {
  padding: 16px 0;
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.tab-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 18px;
  margin: 0;
  color: var(--primary-text-color, #121714);
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

.empty-state p {
  margin-bottom: 16px;
}

.table-container {
  width: 100%;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
  overflow: hidden;
}

.data-table th,
.data-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color, #E5E8EB);
}

.data-table th {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.data-table td {
  font-weight: 400;
  color: var(--primary-text-color, #121714);
}

.badge {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border-radius: 16px;
  padding: 4px 12px;
  font-weight: 500;
  font-size: 14px;
  color: var(--secondary-text-color, #638770);
  display: inline-block;
}

.badge.active {
  background-color: #E3F2FD;
  color: #1976D2;
}

.action-link {
  color: var(--secondary-text-color, #638770);
  font-weight: 700;
  cursor: pointer;
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

@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .data-table {
    display: block;
    overflow-x: auto;
  }
  
  .data-table th {
    white-space: nowrap;
  }
}
</style> 