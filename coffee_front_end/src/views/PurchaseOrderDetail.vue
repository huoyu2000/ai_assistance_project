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
        <h1 class="page-title">{{ order.order_number || '采购订单详情' }}</h1>
      </div>
      <div class="header-buttons">
        <button v-if="canEdit" class="edit-btn" @click="toggleEdit">
          {{ isEditing ? '取消编辑' : '编辑' }}
        </button>
        <button v-if="canConfirm" class="confirm-btn" @click="confirmOrder">确认订单</button>
        <button v-if="canCancel" class="cancel-btn" @click="cancelOrder">取消订单</button>
        <button v-if="isEditing" class="save-btn" @click="saveOrder">保存</button>
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
            <span class="info-label">供应商</span>
            <span class="info-value">{{ order.supplier_name }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">订单日期</span>
            <div v-if="isEditing">
              <input type="date" v-model="editingOrder.order_date" class="edit-input" />
            </div>
            <span v-else class="info-value">{{ formatDate(order.order_date) }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">预计交货日期</span>
            <div v-if="isEditing">
              <input type="date" v-model="editingOrder.expected_delivery_date" class="edit-input" />
            </div>
            <span v-else class="info-value">{{ formatDate(order.expected_delivery_date) || '-' }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">状态</span>
            <span class="info-value status-badge" :class="getOrderStatusClass(order.status)">
              {{ getOrderStatusText(order.status) }}
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">总金额</span>
            <span class="info-value">¥{{ order.total_amount || '0.00' }}</span>
          </div>
          <div class="info-item full-width">
            <span class="info-label">备注</span>
            <div v-if="isEditing">
              <textarea v-model="editingOrder.notes" class="edit-textarea"></textarea>
            </div>
            <span v-else class="info-value">{{ order.notes || '-' }}</span>
          </div>
        </div>
      </div>

      <!-- 订单项目列表 -->
      <div class="items-section">
        <div class="section-header">
          <h2 class="section-title">订单项目</h2>
          <button v-if="isEditing" class="add-item-btn" @click="addOrderItem">添加项目</button>
        </div>
        
        <div v-if="loadingItems" class="loading-container">
          <div class="loading-spinner"></div>
          <p>加载中...</p>
        </div>
        
        <div v-else-if="orderItems.length === 0" class="empty-state">
          <p>暂无订单项目</p>
          <button v-if="isEditing" class="add-item-btn" @click="addOrderItem">添加项目</button>
        </div>
        
        <div v-else class="table-container">
          <table class="items-table">
            <thead>
              <tr>
                <th>产品</th>
                <th>单价</th>
                <th>数量</th>
                <th>单位</th>
                <th>小计</th>
                <th v-if="isEditing">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in orderItems" :key="item.id || index">
                <td>
                  <div v-if="isEditing && item.isEditing">
                    <select v-model="item.product_id" class="edit-select">
                      <option v-for="product in supplierProducts" :key="product.id" :value="product.id">
                        {{ product.product_name }}
                      </option>
                    </select>
                  </div>
                  <span v-else>{{ item.product_name }}</span>
                </td>
                <td>
                  <div v-if="isEditing && item.isEditing">
                    <input type="number" v-model="item.unit_price" class="edit-input" step="0.01" min="0" />
                  </div>
                  <span v-else>¥{{ item.unit_price }}</span>
                </td>
                <td>
                  <div v-if="isEditing && item.isEditing">
                    <input type="number" v-model="item.quantity" class="edit-input" min="1" />
                  </div>
                  <span v-else>{{ item.quantity }}</span>
                </td>
                <td>{{ item.unit }}</td>
                <td>¥{{ calculateSubtotal(item) }}</td>
                <td v-if="isEditing">
                  <div class="action-buttons">
                    <button v-if="item.isEditing" class="save-item-btn" @click="saveItem(item, index)">保存</button>
                    <button v-else class="edit-item-btn" @click="editItem(item)">编辑</button>
                    <button class="delete-item-btn" @click="deleteItem(item, index)">删除</button>
                  </div>
                </td>
              </tr>
            </tbody>
            <tfoot>
              <tr>
                <td colspan="4" class="total-label">总计</td>
                <td colspan="2" class="total-value">¥{{ calculateTotal() }}</td>
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
const isEditing = ref(route.query.edit === 'true');

// 状态变量
const loading = ref(false);
const loadingItems = ref(false);
const error = ref(null);
const order = ref({});
const orderItems = ref([]);
const supplierProducts = ref([]);
const editingOrder = reactive({});

// 获取订单详情
async function fetchOrderData() {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await api.purchase.orders.getById(orderId);
    order.value = response;
    console.log('订单详情:', order.value);
    
    // 复制订单数据到编辑对象
    Object.assign(editingOrder, {
      order_date: order.value.order_date,
      expected_delivery_date: order.value.expected_delivery_date,
      notes: order.value.notes
    });
    
    // 加载订单项目
    fetchOrderItems();
    
    // 如果正在编辑，加载供应商产品
    if (isEditing.value) {
      fetchSupplierProducts();
    }
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
    const response = await api.purchase.orderItems.getByOrderId(orderId);
    orderItems.value = response.map(item => ({
      ...item,
      isEditing: false
    }));
    console.log('订单项目:', orderItems.value);
  } catch (err) {
    console.error('获取订单项目失败:', err);
  } finally {
    loadingItems.value = false;
  }
}

// 获取供应商产品
async function fetchSupplierProducts() {
  try {
    const response = await api.purchase.supplierProducts.getAll({ supplier: order.value.supplier });
    supplierProducts.value = response;
    console.log('供应商产品:', supplierProducts.value);
  } catch (err) {
    console.error('获取供应商产品失败:', err);
  }
}

// 返回上一页
function goBack() {
  router.back();
}

// 切换编辑模式
function toggleEdit() {
  if (isEditing.value) {
    // 取消编辑，重置数据
    isEditing.value = false;
    fetchOrderData();
  } else {
    isEditing.value = true;
    // 加载供应商产品
    fetchSupplierProducts();
  }
}

// 保存订单
async function saveOrder() {
  try {
    const response = await api.purchase.orders.update(orderId, {
      order_date: editingOrder.order_date,
      expected_delivery_date: editingOrder.expected_delivery_date,
      notes: editingOrder.notes
    });
    
    console.log('更新订单成功:', response);
    
    // 重新获取订单数据
    fetchOrderData();
    
    // 退出编辑模式
    isEditing.value = false;
  } catch (err) {
    console.error('更新订单失败:', err);
    alert('更新订单失败，请稍后重试');
  }
}

// 确认订单
async function confirmOrder() {
  if (!confirm('确定要确认此订单吗？确认后将无法编辑。')) {
    return;
  }
  
  try {
    const response = await api.purchase.orders.confirm(orderId);
    console.log('确认订单成功:', response);
    
    // 重新获取订单数据
    fetchOrderData();
  } catch (err) {
    console.error('确认订单失败:', err);
    alert('确认订单失败，请稍后重试');
  }
}

// 取消订单
async function cancelOrder() {
  if (!confirm('确定要取消此订单吗？此操作不可逆。')) {
    return;
  }
  
  try {
    const response = await api.purchase.orders.cancel(orderId);
    console.log('取消订单成功:', response);
    
    // 重新获取订单数据
    fetchOrderData();
  } catch (err) {
    console.error('取消订单失败:', err);
    alert('取消订单失败，请稍后重试');
  }
}

// 添加订单项目
function addOrderItem() {
  orderItems.value.push({
    product_id: null,
    product_name: '',
    unit_price: 0,
    quantity: 1,
    unit: '',
    isEditing: true,
    isNew: true
  });
}

// 编辑项目
function editItem(item) {
  item.isEditing = true;
}

// 保存项目
async function saveItem(item, index) {
  if (!item.product_id) {
    alert('请选择产品');
    return;
  }
  
  try {
    let response;
    
    if (item.isNew) {
      // 创建新项目
      response = await api.purchase.orderItems.create(orderId, {
        product: item.product_id,
        unit_price: parseFloat(item.unit_price),
        quantity: parseInt(item.quantity)
      });
    } else {
      // 更新现有项目
      response = await api.purchase.orderItems.update(orderId, item.id, {
        product: item.product_id,
        unit_price: parseFloat(item.unit_price),
        quantity: parseInt(item.quantity)
      });
    }
    
    console.log('保存订单项目成功:', response);
    
    // 重新获取订单项目
    fetchOrderItems();
  } catch (err) {
    console.error('保存订单项目失败:', err);
    alert('保存订单项目失败，请稍后重试');
  }
}

// 删除项目
async function deleteItem(item, index) {
  if (!confirm('确定要删除此项目吗？')) {
    return;
  }
  
  try {
    if (!item.isNew) {
      // 如果不是新项目，需要调用API删除
      await api.purchase.orderItems.delete(orderId, item.id);
    }
    
    // 从数组中移除
    orderItems.value.splice(index, 1);
    
    console.log('删除订单项目成功');
  } catch (err) {
    console.error('删除订单项目失败:', err);
    alert('删除订单项目失败，请稍后重试');
  }
}

// 计算小计
function calculateSubtotal(item) {
  return (parseFloat(item.unit_price || 0) * parseInt(item.quantity || 0)).toFixed(2);
}

// 计算总计
function calculateTotal() {
  return orderItems.value.reduce((total, item) => {
    return total + parseFloat(item.unit_price || 0) * parseInt(item.quantity || 0);
  }, 0).toFixed(2);
}

// 格式化日期
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN');
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

// 是否可以编辑
const canEdit = computed(() => {
  return order.value.status === 'draft';
});

// 是否可以确认
const canConfirm = computed(() => {
  return order.value.status === 'draft';
});

// 是否可以取消
const canCancel = computed(() => {
  return ['draft', 'submitted', 'approved'].includes(order.value.status);
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

.edit-btn, .confirm-btn, .cancel-btn, .save-btn, .add-item-btn {
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

.edit-btn {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  color: var(--primary-text-color, #121714);
}

.confirm-btn {
  background-color: #E8F5E9;
  color: #388E3C;
}

.cancel-btn {
  background-color: #FFEBEE;
  color: #D32F2F;
}

.save-btn {
  background-color: var(--primary-text-color, #121714);
  color: white;
}

.add-item-btn {
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
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
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

.empty-state p {
  margin-bottom: 16px;
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

.edit-input, .edit-textarea, .edit-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 8px;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.edit-textarea {
  height: 100px;
  resize: vertical;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.edit-item-btn, .save-item-btn, .delete-item-btn {
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
}

.edit-item-btn {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  color: var(--primary-text-color, #121714);
}

.save-item-btn {
  background-color: #E8F5E9;
  color: #388E3C;
}

.delete-item-btn {
  background-color: #FFEBEE;
  color: #D32F2F;
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
</style> 