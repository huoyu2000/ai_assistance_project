<template>
  <div class="page-content-container">
    <div class="header">
    <h1 class="page-title">客户管理</h1>
      <button class="add-customer-btn" @click="openAddCustomerModal">添加客户</button>
    </div>

    <div class="filters">
      <div class="search-bar">
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--secondary-text-color)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <input type="text" placeholder="搜索客户姓名或电话" v-model="searchQuery" @input="handleSearch" />
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchCustomers" class="retry-btn">重试</button>
    </div>

    <div v-else-if="filteredCustomers.length === 0" class="empty-state">
      <p>暂无客户数据</p>
      <button class="add-customer-btn" @click="openAddCustomerModal">添加客户</button>
    </div>

    <div v-else class="customers-table-container">
      <table class="customers-table">
        <thead>
          <tr>
            <th>姓名</th>
            <th>电话</th>
            <th>邮箱</th>
            <th>会员等级</th>
            <th>积分</th>
            <th>注册日期</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="customer in filteredCustomers" :key="customer.customer_id">
            <td>{{ customer.name }}</td>
            <td>{{ customer.phone }}</td>
            <td>{{ customer.email || '-' }}</td>
            <td>{{ getMembershipLevelText(customer.membership_level) }}</td>
            <td>{{ customer.points || 0 }}</td>
            <td>{{ formatDate(customer.created_at) }}</td>
            <td class="actions">
              <span class="action-link" @click="viewCustomerOrders(customer.customer_id)">订单</span>
              <span class="action-link" @click="editCustomer(customer)">编辑</span>
              <span class="action-link" @click="deleteCustomer(customer.customer_id)">删除</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加/编辑客户模态框 -->
    <div v-if="showModal" class="modal-backdrop" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ isEditing ? '编辑客户' : '添加客户' }}</h2>
          <button class="close-btn" @click="closeModal">&times;</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="name">姓名 <span class="required">*</span></label>
            <input id="name" type="text" v-model="customerForm.name" required />
          </div>
          <div class="form-group">
            <label for="phone">电话 <span class="required">*</span></label>
            <input id="phone" type="tel" v-model="customerForm.phone" required />
          </div>
          <div class="form-group">
            <label for="email">邮箱</label>
            <input id="email" type="email" v-model="customerForm.email" />
          </div>
          <div class="form-group">
            <label for="membership_level">会员等级</label>
            <select id="membership_level" v-model="customerForm.membership_level">
              <option value="regular">普通会员</option>
              <option value="silver">银卡会员</option>
              <option value="gold">金卡会员</option>
              <option value="platinum">白金会员</option>
            </select>
          </div>
          <div class="form-group">
            <label for="points">积分</label>
            <input id="points" type="number" v-model="customerForm.points" min="0" />
          </div>
          <div class="form-group">
            <label for="notes">备注</label>
            <textarea id="notes" v-model="customerForm.notes"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="closeModal">取消</button>
          <button class="save-btn" @click="saveCustomer">保存</button>
        </div>
      </div>
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
const customers = ref([]);
const searchQuery = ref('');
const showModal = ref(false);
const isEditing = ref(false);
const customerForm = reactive({
  customer_id: null,
  name: '',
  phone: '',
  email: '',
  membership_level: 'regular',
  points: 0,
  notes: ''
});

// 获取客户列表
async function fetchCustomers() {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await api.sales.customers.getAll();
    customers.value = response;
    console.log('获取到客户数据:', response);
  } catch (err) {
    console.error('获取客户列表失败:', err);
    error.value = '获取客户列表失败，请稍后重试';
  } finally {
    loading.value = false;
  }
}

// 过滤客户
const filteredCustomers = computed(() => {
  if (!searchQuery.value) return customers.value;
  
  const query = searchQuery.value.toLowerCase();
  return customers.value.filter(customer => 
    (customer.name && customer.name.toLowerCase().includes(query)) ||
    (customer.phone && customer.phone.includes(query))
  );
});

// 搜索处理
function handleSearch() {
  console.log('搜索:', searchQuery.value);
}

// 打开添加客户模态框
function openAddCustomerModal() {
  isEditing.value = false;
  resetCustomerForm();
  showModal.value = true;
}

// 编辑客户
function editCustomer(customer) {
  isEditing.value = true;
  Object.assign(customerForm, customer);
  showModal.value = true;
}

// 查看客户订单
function viewCustomerOrders(customerId) {
  router.push(`/customers/${customerId}/orders`);
}

// 删除客户
async function deleteCustomer(customerId) {
  if (!confirm('确定要删除此客户吗？此操作不可逆。')) {
    return;
  }
  
  try {
    loading.value = true;
    await api.sales.customers.delete(customerId);
    await fetchCustomers(); // 重新加载客户列表
    console.log('客户已删除:', customerId);
  } catch (err) {
    console.error('删除客户失败:', err);
    alert('删除客户失败，请稍后重试');
  } finally {
    loading.value = false;
  }
}

// 保存客户
async function saveCustomer() {
  if (!validateCustomerForm()) {
    return;
  }
  
  try {
    loading.value = true;
    
    if (isEditing.value) {
      // 更新客户
      await api.sales.customers.update(customerForm.customer_id, customerForm);
      console.log('客户已更新:', customerForm.customer_id);
    } else {
      // 创建客户
      await api.sales.customers.create(customerForm);
      console.log('客户已创建');
    }
    
    await fetchCustomers(); // 重新加载客户列表
    closeModal();
  } catch (err) {
    console.error('保存客户失败:', err);
    alert('保存客户失败，请稍后重试');
  } finally {
    loading.value = false;
  }
}

// 验证客户表单
function validateCustomerForm() {
  if (!customerForm.name) {
    alert('请输入客户姓名');
    return false;
  }
  
  if (!customerForm.phone) {
    alert('请输入客户电话');
    return false;
  }
  
  return true;
}

// 重置客户表单
function resetCustomerForm() {
  customerForm.customer_id = null;
  customerForm.name = '';
  customerForm.phone = '';
  customerForm.email = '';
  customerForm.membership_level = 'regular';
  customerForm.points = 0;
  customerForm.notes = '';
}

// 关闭模态框
function closeModal() {
  showModal.value = false;
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

// 格式化日期
function formatDate(dateString) {
  if (!dateString) return '';
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN');
}

// 初始化
onMounted(() => {
  console.log('客户管理页面已加载');
  fetchCustomers();
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

.add-customer-btn {
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

.customers-table-container {
  padding: 16px;
  width: 100%;
  overflow-x: auto;
}

.customers-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
  overflow: hidden;
}

.customers-table th,
.customers-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color, #E5E8EB);
}

.customers-table th {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.customers-table td {
  font-weight: 400;
  color: var(--primary-text-color, #121714);
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

/* 模态框样式 */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: var(--content-bg-color, #FFFFFF);
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid var(--border-color, #DBE5DE);
}

.modal-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: var(--primary-text-color, #121714);
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--secondary-text-color, #638770);
}

.modal-body {
  padding: 16px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 8px;
  color: var(--primary-text-color, #121714);
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 8px;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.form-group textarea {
  height: 100px;
  resize: vertical;
}

.required {
  color: red;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px;
  border-top: 1px solid var(--border-color, #DBE5DE);
}

.cancel-btn, .save-btn {
  padding: 8px 16px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  cursor: pointer;
  border: none;
}

.cancel-btn {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  color: var(--primary-text-color, #121714);
}

.save-btn {
  background-color: var(--primary-text-color, #121714);
  color: white;
}

@media (max-width: 768px) {
  .customers-table {
    display: block;
    overflow-x: auto;
  }
  
  .customers-table th {
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