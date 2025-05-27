<template>
  <div class="page-content-container">
    <div class="header">
      <h1 class="page-title">供应商</h1>
      <button class="add-supplier-btn" @click="showAddSupplierModal = true">添加供应商</button>
    </div>

    <div class="search-bar">
      <div class="search-input">
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--secondary-text-color)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <input type="text" placeholder="搜索供应商" v-model="searchQuery" @input="handleSearch" />
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchSuppliers" class="retry-btn">重试</button>
    </div>

    <div v-else class="supplier-table-container">
      <table class="supplier-table">
        <thead>
          <tr>
            <th class="th-name">供应商</th>
            <th class="th-category">类别</th>
            <th class="th-contact">联系人</th>
            <th class="th-phone">电话</th>
            <th class="th-status">状态</th>
            <th class="th-action">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="supplier in suppliers" :key="supplier.supplier_id">
            <td class="td-name">{{ supplier.name }}</td>
            <td class="td-category">{{ supplier.category || '未分类' }}</td>
            <td class="td-contact">{{ supplier.contact_name || '-' }}</td>
            <td class="td-phone">{{ supplier.phone || '-' }}</td>
            <td class="td-status">
              <span class="status-badge" :class="{ 'inactive': supplier.status === 'INACTIVE' }">
                {{ getStatusText(supplier.status) }}
              </span>
            </td>
            <td class="td-action">
              <span class="edit-link" @click="editSupplier(supplier)">编辑</span>
              <span class="view-link" @click="viewSupplierDetails(supplier.supplier_id)">查看</span>
            </td>
          </tr>
          <tr v-if="suppliers.length === 0">
            <td colspan="6" class="no-data">暂无供应商数据</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加供应商模态框 -->
    <div class="modal-overlay" v-if="showAddSupplierModal" @click.self="showAddSupplierModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>添加供应商</h3>
          <button class="close-btn" @click="showAddSupplierModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="supplier-name">供应商名称 <span class="required">*</span></label>
            <input type="text" id="supplier-name" v-model="newSupplier.name" placeholder="输入供应商名称">
          </div>
          <div class="form-group">
            <label for="supplier-category">类别</label>
            <input type="text" id="supplier-category" v-model="newSupplier.category" placeholder="输入供应商类别">
          </div>
          <div class="form-group">
            <label for="supplier-contact">联系人</label>
            <input type="text" id="supplier-contact" v-model="newSupplier.contact_name" placeholder="输入联系人姓名">
          </div>
          <div class="form-group">
            <label for="supplier-phone">电话</label>
            <input type="text" id="supplier-phone" v-model="newSupplier.phone" placeholder="输入联系电话">
          </div>
          <div class="form-group">
            <label for="supplier-email">邮箱</label>
            <input type="email" id="supplier-email" v-model="newSupplier.email" placeholder="输入邮箱地址">
          </div>
          <div class="form-group">
            <label for="supplier-address">地址</label>
            <textarea id="supplier-address" v-model="newSupplier.address" placeholder="输入供应商地址"></textarea>
          </div>
          <div class="form-group">
            <label for="supplier-status">状态</label>
            <select id="supplier-status" v-model="newSupplier.status">
              <option value="ACTIVE">活跃</option>
              <option value="INACTIVE">停用</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showAddSupplierModal = false">取消</button>
          <button class="submit-btn" @click="addSupplier" :disabled="submitting">
            {{ submitting ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 编辑供应商模态框 -->
    <div class="modal-overlay" v-if="showEditSupplierModal" @click.self="showEditSupplierModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>编辑供应商</h3>
          <button class="close-btn" @click="showEditSupplierModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="edit-supplier-name">供应商名称 <span class="required">*</span></label>
            <input type="text" id="edit-supplier-name" v-model="editingSupplier.name" placeholder="输入供应商名称">
          </div>
          <div class="form-group">
            <label for="edit-supplier-category">类别</label>
            <input type="text" id="edit-supplier-category" v-model="editingSupplier.category" placeholder="输入供应商类别">
          </div>
          <div class="form-group">
            <label for="edit-supplier-contact">联系人</label>
            <input type="text" id="edit-supplier-contact" v-model="editingSupplier.contact_name" placeholder="输入联系人姓名">
          </div>
          <div class="form-group">
            <label for="edit-supplier-phone">电话</label>
            <input type="text" id="edit-supplier-phone" v-model="editingSupplier.phone" placeholder="输入联系电话">
          </div>
          <div class="form-group">
            <label for="edit-supplier-email">邮箱</label>
            <input type="email" id="edit-supplier-email" v-model="editingSupplier.email" placeholder="输入邮箱地址">
          </div>
          <div class="form-group">
            <label for="edit-supplier-address">地址</label>
            <textarea id="edit-supplier-address" v-model="editingSupplier.address" placeholder="输入供应商地址"></textarea>
          </div>
          <div class="form-group">
            <label for="edit-supplier-status">状态</label>
            <select id="edit-supplier-status" v-model="editingSupplier.status">
              <option value="ACTIVE">活跃</option>
              <option value="INACTIVE">停用</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showEditSupplierModal = false">取消</button>
          <button class="submit-btn" @click="updateSupplier" :disabled="submitting">
            {{ submitting ? '更新中...' : '更新' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import api from '../api/api';

const router = useRouter();

// 状态变量
const loading = ref(false);
const submitting = ref(false);
const error = ref(null);
const suppliers = ref([]);
const searchQuery = ref('');
const showAddSupplierModal = ref(false);
const showEditSupplierModal = ref(false);

// 新供应商数据
const newSupplier = reactive({
  name: '',
  category: '',
  contact_name: '',
  phone: '',
  email: '',
  address: '',
  status: 'ACTIVE'
});

// 编辑供应商数据
const editingSupplier = reactive({
  supplier_id: null,
  name: '',
  category: '',
  contact_name: '',
  phone: '',
  email: '',
  address: '',
  status: 'ACTIVE'
});

// 获取供应商列表
async function fetchSuppliers() {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await api.purchase.suppliers.getAll();
    console.log('获取到供应商数据:', response);
    suppliers.value = response;
  } catch (err) {
    console.error('获取供应商列表失败:', err);
    error.value = '获取供应商列表失败，请稍后重试';
  } finally {
    loading.value = false;
  }
}

// 状态文本转换
function getStatusText(status) {
  const statusMap = {
    'ACTIVE': '活跃',
    'INACTIVE': '停用'
  };
  return statusMap[status] || status;
}

// 搜索处理
function handleSearch() {
  // 这里可以实现实时搜索逻辑，或者使用防抖函数
  console.log('搜索:', searchQuery.value);
}

// 查看供应商详情
function viewSupplierDetails(supplierId) {
  router.push(`/procurement/supplier/${supplierId}`);
}

// 编辑供应商
function editSupplier(supplier) {
  console.log('编辑供应商:', supplier);
  Object.assign(editingSupplier, {
    supplier_id: supplier.supplier_id,
    name: supplier.name || '',
    category: supplier.category || '',
    contact_name: supplier.contact_name || '',
    phone: supplier.phone || '',
    email: supplier.email || '',
    address: supplier.address || '',
    status: supplier.status || 'ACTIVE'
  });
  
  showEditSupplierModal.value = true;
}

// 添加供应商
async function addSupplier() {
  // 表单验证
  if (!newSupplier.name) {
    alert('请填写供应商名称');
    return;
  }
  
  submitting.value = true;
  
  try {
    const response = await api.purchase.suppliers.create({
      name: newSupplier.name,
      category: newSupplier.category || null,
      contact_name: newSupplier.contact_name || null,
      phone: newSupplier.phone || null,
      email: newSupplier.email || null,
      address: newSupplier.address || null,
      status: newSupplier.status
    });
    
    console.log('添加供应商成功:', response);
    
    // 重置表单并关闭模态框
    Object.assign(newSupplier, {
      name: '',
      category: '',
      contact_name: '',
      phone: '',
      email: '',
      address: '',
      status: 'ACTIVE'
    });
    
    showAddSupplierModal.value = false;
    
    // 重新获取供应商列表
    await fetchSuppliers();
  } catch (err) {
    console.error('添加供应商失败:', err);
    alert('添加供应商失败，请稍后重试');
  } finally {
    submitting.value = false;
  }
}

// 更新供应商
async function updateSupplier() {
  // 表单验证
  if (!editingSupplier.name) {
    alert('请填写供应商名称');
    return;
  }
  
  submitting.value = true;
  
  try {
    const response = await api.purchase.suppliers.update(editingSupplier.supplier_id, {
      name: editingSupplier.name,
      category: editingSupplier.category || null,
      contact_name: editingSupplier.contact_name || null,
      phone: editingSupplier.phone || null,
      email: editingSupplier.email || null,
      address: editingSupplier.address || null,
      status: editingSupplier.status
    });
    
    console.log('更新供应商成功:', response);
    
    showEditSupplierModal.value = false;
    
    // 重新获取供应商列表
    await fetchSuppliers();
  } catch (err) {
    console.error('更新供应商失败:', err);
    alert('更新供应商失败，请稍后重试');
  } finally {
    submitting.value = false;
  }
}

// 初始化
onMounted(async () => {
  console.log('采购管理页面已加载');
  await fetchSuppliers();
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

.add-supplier-btn {
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

.search-bar {
  padding: 12px 16px;
  width: 100%;
}

.search-input {
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

.search-input input {
  flex: 1;
  border: none;
  background: transparent;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  color: var(--primary-text-color, #121714);
  outline: none;
  width: 100%;
}

.search-input input::placeholder {
  color: var(--secondary-text-color, #638770);
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

.supplier-table-container {
  padding: 0 16px 16px;
  width: 100%;
  overflow-x: auto;
}

.supplier-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
  overflow: hidden;
}

.supplier-table th,
.supplier-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color, #E5E8EB);
}

.supplier-table th {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.supplier-table td {
  font-weight: 400;
  color: var(--primary-text-color, #121714);
  height: 72px;
}

.th-action, .td-action {
  text-align: center;
}

.th-name, .td-name {
  min-width: 200px;
}

.th-category, .td-category,
.th-contact, .td-contact,
.th-phone, .td-phone,
.th-status, .td-status,
.th-action, .td-action {
  text-align: center;
  min-width: 100px;
}

.td-category, .td-contact, .td-phone {
  color: var(--secondary-text-color, #638770);
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
  background-color: #FFE0E0;
  color: #E53935;
}

.view-link, .edit-link {
  color: var(--secondary-text-color, #638770);
  font-weight: 700;
  cursor: pointer;
  margin: 0 5px;
}

.no-data {
  text-align: center;
  color: var(--secondary-text-color, #638770);
  padding: 24px 0;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: var(--content-bg-color, #FFFFFF);
  border-radius: 12px;
  width: 500px;
  max-width: 90%;
  max-height: 90%;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid var(--border-color, #DBE5DE);
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--primary-text-color, #121714);
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: var(--secondary-text-color, #638770);
  cursor: pointer;
}

.modal-body {
  padding: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--primary-text-color, #121714);
}

.required {
  color: red;
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

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-color, #DBE5DE);
}

.cancel-btn {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 500;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
  cursor: pointer;
}

.submit-btn {
  background-color: var(--primary-text-color, #121714);
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 500;
  font-size: 14px;
  color: white;
  cursor: pointer;
}

.submit-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .supplier-table {
    display: block;
    overflow-x: auto;
  }
  
  .supplier-table th {
    white-space: nowrap;
  }
}

/* 修复页面宽度超过1024px的问题 */
@media (min-width: 1024px) {
  .page-content-container {
    width: 100%;
    max-width: 100%;
  }
  
  .supplier-table-container {
    width: 100%;
  }
  
  .supplier-table {
    width: 100%;
  }
}
</style> 