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
        <h1 class="page-title">创建采购订单</h1>
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else class="create-order-content">
      <!-- 订单基本信息 -->
      <div class="info-card">
        <h2 class="card-title">订单信息</h2>
        <div class="info-grid">
          <div class="info-item">
            <label for="supplier">供应商 <span class="required">*</span></label>
            <select id="supplier" v-model="orderData.supplier" class="form-input" @change="handleSupplierChange">
              <option value="">请选择供应商</option>
              <option v-for="supplier in suppliers" :key="supplier.supplier_id" :value="supplier.supplier_id">
                {{ supplier.name }}
              </option>
            </select>
          </div>
          <div class="info-item">
            <label for="order-date">订单日期 <span class="required">*</span></label>
            <input type="date" id="order-date" v-model="orderData.order_date" class="form-input" />
          </div>
          <div class="info-item">
            <label for="expected-delivery-date">预计交货日期</label>
            <input type="date" id="expected-delivery-date" v-model="orderData.expected_delivery_date" class="form-input" />
          </div>
          <div class="info-item full-width">
            <label for="notes">备注</label>
            <textarea id="notes" v-model="orderData.notes" class="form-textarea" placeholder="输入订单备注信息"></textarea>
          </div>
        </div>
      </div>

      <!-- 订单项目列表 -->
      <div class="items-section">
        <div class="section-header">
          <h2 class="section-title">订单项目</h2>
          <button class="add-item-btn" @click="addOrderItem" :disabled="!orderData.supplier">添加项目</button>
        </div>
        
        <div v-if="!orderData.supplier" class="empty-state">
          <p>请先选择供应商</p>
        </div>
        
        <div v-else-if="orderItems.length === 0" class="empty-state">
          <p>暂无订单项目</p>
          <button class="add-item-btn" @click="addOrderItem">添加项目</button>
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
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in orderItems" :key="index">
                <td>
                  <select v-model="item.product_id" class="form-select" @change="handleProductChange(item, index)">
                    <option value="">请选择产品</option>
                    <option v-for="product in supplierProducts" :key="product.id" :value="product.id">
                      {{ product.product_name }}
                    </option>
                  </select>
                </td>
                <td>
                  <input type="number" v-model="item.unit_price" class="form-input" step="0.01" min="0" @input="updateTotals" />
                </td>
                <td>
                  <input type="number" v-model="item.quantity" class="form-input" min="1" @input="updateTotals" />
                </td>
                <td>{{ item.unit }}</td>
                <td>¥{{ calculateSubtotal(item) }}</td>
                <td>
                  <button class="delete-item-btn" @click="deleteItem(index)">删除</button>
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

      <div class="actions-bar">
        <button class="cancel-btn" @click="goBack">取消</button>
        <button class="save-btn" @click="saveAsDraft">保存为草稿</button>
        <button class="submit-btn" @click="submitOrder">提交订单</button>
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

// 获取URL参数中的供应商ID
const preselectedSupplierId = route.query.supplier;

// 状态变量
const loading = ref(false);
const suppliers = ref([]);
const supplierProducts = ref([]);
const orderItems = ref([]);

// 订单数据
const orderData = reactive({
  supplier: preselectedSupplierId || '',
  order_date: new Date().toISOString().split('T')[0], // 默认今天
  expected_delivery_date: '',
  notes: ''
});

// 获取供应商列表
async function fetchSuppliers() {
  loading.value = true;
  
  try {
    const response = await api.purchase.suppliers.getAll();
    suppliers.value = response;
    console.log('获取到供应商数据:', response);
    
    // 如果URL中有预选的供应商，加载其产品
    if (preselectedSupplierId) {
      await handleSupplierChange();
    }
  } catch (err) {
    console.error('获取供应商列表失败:', err);
  } finally {
    loading.value = false;
  }
}

// 处理供应商变化
async function handleSupplierChange() {
  if (!orderData.supplier) {
    supplierProducts.value = [];
    orderItems.value = [];
    return;
  }
  
  try {
    const response = await api.purchase.suppliers.getProducts(orderData.supplier);
    supplierProducts.value = response;
    console.log('获取到供应商产品:', response);
  } catch (err) {
    console.error('获取供应商产品失败:', err);
  }
}

// 添加订单项目
function addOrderItem() {
  orderItems.value.push({
    product_id: '',
    product_name: '',
    unit_price: 0,
    quantity: 1,
    unit: ''
  });
}

// 处理产品变化
function handleProductChange(item, index) {
  if (!item.product_id) {
    item.unit_price = 0;
    item.unit = '';
    return;
  }
  
  const selectedProduct = supplierProducts.value.find(p => p.id === item.product_id);
  if (selectedProduct) {
    item.product_name = selectedProduct.product_name;
    item.unit_price = selectedProduct.price;
    item.unit = selectedProduct.product_unit;
    
    // 更新小计和总计
    updateTotals();
  }
}

// 删除项目
function deleteItem(index) {
  orderItems.value.splice(index, 1);
  updateTotals();
}

// 更新总计
function updateTotals() {
  console.log('更新总计');
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

// 验证表单
function validateForm() {
  if (!orderData.supplier) {
    alert('请选择供应商');
    return false;
  }
  
  if (!orderData.order_date) {
    alert('请选择订单日期');
    return false;
  }
  
  if (orderItems.value.length === 0) {
    alert('请添加至少一个订单项目');
    return false;
  }
  
  for (const item of orderItems.value) {
    if (!item.product_id) {
      alert('请为所有订单项目选择产品');
      return false;
    }
    
    if (!item.unit_price || parseFloat(item.unit_price) <= 0) {
      alert('所有订单项目的单价必须大于0');
      return false;
    }
    
    if (!item.quantity || parseInt(item.quantity) <= 0) {
      alert('所有订单项目的数量必须大于0');
      return false;
    }
  }
  
  return true;
}

// 保存为草稿
async function saveAsDraft() {
  if (!orderData.supplier || !orderData.order_date) {
    alert('请选择供应商和订单日期');
    return;
  }
  
  try {
    loading.value = true;
    
    // 创建订单
    const orderResponse = await api.purchase.orders.create({
      supplier: orderData.supplier,
      order_date: orderData.order_date,
      expected_delivery_date: orderData.expected_delivery_date || null,
      notes: orderData.notes || null,
      status: 'draft'
    });
    
    console.log('创建订单成功:', orderResponse);
    
    // 如果有订单项目，添加它们
    if (orderItems.value.length > 0 && orderResponse.order_id) {
      for (const item of orderItems.value) {
        if (item.product_id) {
          await api.purchase.orderItems.create(orderResponse.order_id, {
            product: item.product_id,
            unit_price: parseFloat(item.unit_price),
            quantity: parseInt(item.quantity)
          });
        }
      }
    }
    
    alert('订单已保存为草稿');
    
    // 跳转到订单详情页
    if (orderResponse.order_id) {
      router.push(`/procurement/orders/${orderResponse.order_id}`);
    } else {
      router.push('/procurement/orders');
    }
  } catch (err) {
    console.error('保存订单失败:', err);
    alert('保存订单失败，请稍后重试');
  } finally {
    loading.value = false;
  }
}

// 提交订单
async function submitOrder() {
  if (!validateForm()) {
    return;
  }
  
  try {
    loading.value = true;
    
    // 创建订单
    const orderResponse = await api.purchase.orders.create({
      supplier: orderData.supplier,
      order_date: orderData.order_date,
      expected_delivery_date: orderData.expected_delivery_date || null,
      notes: orderData.notes || null,
      status: 'submitted'
    });
    
    console.log('创建订单成功:', orderResponse);
    
    // 添加订单项目
    if (orderItems.value.length > 0 && orderResponse.order_id) {
      for (const item of orderItems.value) {
        await api.purchase.orderItems.create(orderResponse.order_id, {
          product: item.product_id,
          unit_price: parseFloat(item.unit_price),
          quantity: parseInt(item.quantity)
        });
      }
    }
    
    alert('订单已提交');
    
    // 跳转到订单详情页
    if (orderResponse.order_id) {
      router.push(`/procurement/orders/${orderResponse.order_id}`);
    } else {
      router.push('/procurement/orders');
    }
  } catch (err) {
    console.error('提交订单失败:', err);
    alert('提交订单失败，请稍后重试');
  } finally {
    loading.value = false;
  }
}

// 返回上一页
function goBack() {
  router.back();
}

// 初始化
onMounted(() => {
  console.log('创建采购订单页面已加载');
  fetchSuppliers();
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

.loading-container {
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

.create-order-content {
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
  gap: 8px;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-item label {
  font-size: 14px;
  font-weight: 500;
  color: var(--primary-text-color, #121714);
}

.required {
  color: red;
}

.form-input, .form-textarea, .form-select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 8px;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.form-textarea {
  height: 100px;
  resize: vertical;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.add-item-btn {
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

.add-item-btn:disabled {
  background-color: #E0E0E0;
  color: #9E9E9E;
  cursor: not-allowed;
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

.items-table input, .items-table select {
  width: 100%;
  padding: 8px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 4px;
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

.delete-item-btn {
  background-color: #FFEBEE;
  color: #D32F2F;
  border: none;
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  cursor: pointer;
}

.actions-bar {
  display: flex;
  justify-content: flex-end;
  gap: 16px;
  margin-top: 24px;
}

.cancel-btn, .save-btn, .submit-btn {
  border: none;
  border-radius: 8px;
  padding: 0 24px;
  height: 40px;
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 500;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cancel-btn {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  color: var(--primary-text-color, #121714);
}

.save-btn {
  background-color: #E3F2FD;
  color: #1976D2;
}

.submit-btn {
  background-color: var(--primary-text-color, #121714);
  color: white;
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
  
  .actions-bar {
    flex-direction: column;
    align-items: stretch;
  }
}
</style> 