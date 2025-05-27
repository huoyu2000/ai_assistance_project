<template>
  <div class="page-content-container">
    <div class="header">
      <h1 class="page-title">产品</h1>
      <div class="header-buttons">
        <button class="add-btn" @click="showAddCategoryModal = true">添加分类</button>
        <button class="add-btn" @click="showAddProductModal = true">添加产品</button>
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

    <div class="search-bar">
      <div class="search-input">
        <div class="search-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--secondary-text-color)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="8"></circle>
            <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
          </svg>
        </div>
        <input type="text" placeholder="搜索产品" v-model="searchQuery" />
      </div>
    </div>

    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>

    <div v-else-if="error" class="error-container">
      <p>{{ error }}</p>
      <button @click="fetchProducts" class="retry-btn">重试</button>
    </div>

    <div v-else-if="activeTab === 'category'" class="category-container">
      <table class="category-table">
        <thead>
          <tr>
            <th class="th-name">分类名称</th>
            <th class="th-order">排序</th>
            <th class="th-action">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.category_id">
            <td class="td-name">{{ category.name }}</td>
            <td class="td-order">{{ category.sort_order }}</td>
            <td class="td-action">
              <span class="edit-link" @click="editCategory(category)">编辑</span>
              <span class="delete-link" @click="confirmDeleteCategory(category)">删除</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-else class="product-table-container">
      <table class="product-table">
        <thead>
          <tr>
            <th class="th-name">产品名称</th>
            <th class="th-category">类别</th>
            <th class="th-stock">库存</th>
            <th class="th-price">价格</th>
            <th class="th-status">状态</th>
            <th class="th-action">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(product, index) in filteredProducts" :key="product && product.product_id ? product.product_id : index">
            <td class="td-name">{{ product && product.name ? product.name : '未命名' }}</td>
            <td class="td-category">{{ product && product.category_name ? product.category_name : '未分类' }}</td>
            <td class="td-stock">{{ product && product.inventory_qty !== undefined ? product.inventory_qty : 0 }} {{ product && product.unit ? product.unit : '个' }}</td>
            <td class="td-price">¥{{ product && product.price !== undefined ? product.price : 0 }}</td>
            <td class="td-status"><span class="status-badge">{{ product && product.status ? getStatusText(product.status) : '未知' }}</span></td>
            <td class="td-action">
              <span class="edit-link" @click="product && editProduct(product)">编辑</span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 添加分类模态框 -->
    <div class="modal-overlay" v-if="showAddCategoryModal" @click.self="showAddCategoryModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>添加分类</h3>
          <button class="close-btn" @click="showAddCategoryModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="category-name">分类名称 <span class="required">*</span></label>
            <input type="text" id="category-name" v-model="newCategory.name" placeholder="输入分类名称">
          </div>
          <div class="form-group">
            <label for="category-sort">排序</label>
            <input type="number" id="category-sort" v-model="newCategory.sort_order" placeholder="输入排序值">
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showAddCategoryModal = false">取消</button>
          <button class="submit-btn" @click="addCategory" :disabled="submitting">
            {{ submitting ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 编辑分类模态框 -->
    <div class="modal-overlay" v-if="showEditCategoryModal" @click.self="showEditCategoryModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>编辑分类</h3>
          <button class="close-btn" @click="showEditCategoryModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="edit-category-name">分类名称 <span class="required">*</span></label>
            <input type="text" id="edit-category-name" v-model="editingCategory.name" placeholder="输入分类名称">
          </div>
          <div class="form-group">
            <label for="edit-category-sort">排序</label>
            <input type="number" id="edit-category-sort" v-model="editingCategory.sort_order" placeholder="输入排序值">
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showEditCategoryModal = false">取消</button>
          <button class="submit-btn" @click="updateCategory" :disabled="submitting">
            {{ submitting ? '更新中...' : '更新' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 删除分类确认模态框 -->
    <div class="modal-overlay" v-if="showDeleteCategoryModal" @click.self="showDeleteCategoryModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>删除分类</h3>
          <button class="close-btn" @click="showDeleteCategoryModal = false">×</button>
        </div>
        <div class="modal-body">
          <p>确定要删除分类 "{{ categoryToDelete?.name }}" 吗？</p>
          <p class="warning-text">注意：删除分类可能会影响关联的产品。</p>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showDeleteCategoryModal = false">取消</button>
          <button class="delete-btn" @click="deleteCategory" :disabled="submitting">
            {{ submitting ? '删除中...' : '确认删除' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 添加产品模态框 -->
    <div class="modal-overlay" v-if="showAddProductModal" @click.self="showAddProductModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>添加产品</h3>
          <button class="close-btn" @click="showAddProductModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="product-name">产品名称 <span class="required">*</span></label>
            <input type="text" id="product-name" v-model="newProduct.name" placeholder="输入产品名称">
          </div>
          <div class="form-group">
            <label for="product-category">类别 <span class="required">*</span></label>
            <select id="product-category" v-model="newProduct.category_id">
              <option value="">选择类别</option>
              <option v-for="category in categories" :key="category.category_id" :value="category.category_id">
                {{ category.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label for="product-sku">SKU</label>
            <input type="text" id="product-sku" v-model="newProduct.sku" placeholder="输入SKU编码">
          </div>
          <div class="form-group">
            <label for="product-unit">单位 <span class="required">*</span></label>
            <input type="text" id="product-unit" v-model="newProduct.unit" placeholder="输入单位">
          </div>
          <div class="form-group">
            <label for="product-price">价格 <span class="required">*</span></label>
            <input type="number" id="product-price" v-model="newProduct.price" placeholder="输入价格">
          </div>
          <div class="form-group">
            <label for="product-inventory">库存数量</label>
            <input type="number" id="product-inventory" v-model="newProduct.inventory_qty" placeholder="输入库存数量">
          </div>
          <div class="form-group">
            <label for="product-reorder">补货点</label>
            <input type="number" id="product-reorder" v-model="newProduct.reorder_point" placeholder="输入补货点">
          </div>
          <div class="form-group">
            <label for="product-status">状态</label>
            <select id="product-status" v-model="newProduct.status">
              <option value="ACTIVE">在售</option>
              <option value="INACTIVE">下架</option>
              <option value="OUT_OF_STOCK">缺货</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showAddProductModal = false">取消</button>
          <button class="submit-btn" @click="addProduct" :disabled="submitting">
            {{ submitting ? '保存中...' : '保存' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 编辑产品模态框 -->
    <div class="modal-overlay" v-if="showEditProductModal" @click.self="showEditProductModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>编辑产品</h3>
          <button class="close-btn" @click="showEditProductModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="edit-product-name">产品名称 <span class="required">*</span></label>
            <input type="text" id="edit-product-name" v-model="editingProduct.name" placeholder="输入产品名称">
          </div>
          <div class="form-group">
            <label for="edit-product-category">类别 <span class="required">*</span></label>
            <select id="edit-product-category" v-model="editingProduct.category_id">
              <option value="">选择类别</option>
              <option v-for="category in categories" :key="category.category_id" :value="category.category_id">
                {{ category.name }} (ID: {{ category.category_id }})
              </option>
            </select>
          </div>
          <div class="debug-info" style="font-size: 12px; color: #999; margin-top: 4px;">
            当前选择的分类ID: {{ editingProduct.category_id }}
          </div>
          <div class="form-group">
            <label for="edit-product-sku">SKU</label>
            <input type="text" id="edit-product-sku" v-model="editingProduct.sku" placeholder="输入SKU编码">
          </div>
          <div class="form-group">
            <label for="edit-product-unit">单位 <span class="required">*</span></label>
            <input type="text" id="edit-product-unit" v-model="editingProduct.unit" placeholder="输入单位">
          </div>
          <div class="form-group">
            <label for="edit-product-price">价格 <span class="required">*</span></label>
            <input type="number" id="edit-product-price" v-model="editingProduct.price" placeholder="输入价格">
          </div>
          <div class="form-group">
            <label for="edit-product-inventory">库存数量</label>
            <input type="number" id="edit-product-inventory" v-model="editingProduct.inventory_qty" placeholder="输入库存数量">
          </div>
          <div class="form-group">
            <label for="edit-product-reorder">补货点</label>
            <input type="number" id="edit-product-reorder" v-model="editingProduct.reorder_point" placeholder="输入补货点">
          </div>
          <div class="form-group">
            <label for="edit-product-status">状态</label>
            <select id="edit-product-status" v-model="editingProduct.status">
              <option value="ACTIVE">在售</option>
              <option value="INACTIVE">下架</option>
              <option value="OUT_OF_STOCK">缺货</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showEditProductModal = false">取消</button>
          <button class="submit-btn" @click="updateProduct" :disabled="submitting">
            {{ submitting ? '更新中...' : '更新' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import api from '../api/api';

// 选项卡
const tabs = [
  { id: 'all', name: '所有产品' },
  { id: 'category', name: '分类管理' },
  { id: 'recipe', name: '菜谱' },
  { id: 'pricing', name: '定价' }
];
const activeTab = ref('all');

// 状态变量
const loading = ref(false);
const submitting = ref(false);
const error = ref(null);
const products = ref([]);
const categories = ref([]);
const searchQuery = ref('');
const showAddProductModal = ref(false);
const showEditProductModal = ref(false);
const showAddCategoryModal = ref(false);
const showEditCategoryModal = ref(false);
const showDeleteCategoryModal = ref(false);
const categoryToDelete = ref(null);

// 过滤后的产品列表
const filteredProducts = computed(() => {
  if (!searchQuery.value) {
    return products.value || [];
  } else {
    const query = searchQuery.value.toLowerCase();
    return (products.value || []).filter(product => 
      product && product.name && product.name.toLowerCase().includes(query) || 
      (product && product.category_name && product.category_name.toLowerCase().includes(query))
    );
  }
});

// 获取产品列表
async function fetchProducts() {
  loading.value = true;
  error.value = null;
  
  try {
    const response = await api.product.products.getAll();
    products.value = response;
  } catch (err) {
    console.error('获取产品列表失败:', err);
    error.value = '获取产品列表失败，请稍后重试';
  } finally {
    loading.value = false;
  }
}

// 获取分类列表
async function fetchCategories() {
  try {
    const response = await api.product.categories.getAll();
    categories.value = response;
  } catch (err) {
    console.error('获取分类列表失败:', err);
  }
}

// 状态文本转换
function getStatusText(status) {
  const statusMap = {
    'ACTIVE': '在售',
    'INACTIVE': '下架',
    'OUT_OF_STOCK': '缺货'
  };
  return statusMap[status] || status;
}

// 添加分类
const newCategory = reactive({
  name: '',
  sort_order: 0
});

async function addCategory() {
  // 表单验证
  if (!newCategory.name) {
    alert('请填写分类名称');
    return;
  }
  
  submitting.value = true;
  
  try {
    await api.product.categories.create({
      name: newCategory.name,
      sort_order: parseInt(newCategory.sort_order) || 0
    });
    
    // 重置表单并关闭模态框
    Object.assign(newCategory, {
      name: '',
      sort_order: 0
    });
    
    showAddCategoryModal.value = false;
    
    // 重新获取分类列表
    await fetchCategories();
  } catch (err) {
    console.error('添加分类失败:', err);
    alert('添加分类失败，请稍后重试');
  } finally {
    submitting.value = false;
  }
}

// 编辑分类
const editingCategory = reactive({
  category_id: null,
  name: '',
  sort_order: 0
});

function editCategory(category) {
  editingCategory.category_id = category.category_id;
  editingCategory.name = category.name;
  editingCategory.sort_order = category.sort_order;
  
  showEditCategoryModal.value = true;
}

async function updateCategory() {
  // 表单验证
  if (!editingCategory.name) {
    alert('请填写分类名称');
    return;
  }
  
  submitting.value = true;
  
  try {
    await api.product.categories.update(editingCategory.category_id, {
      name: editingCategory.name,
      sort_order: parseInt(editingCategory.sort_order) || 0
    });
    
    showEditCategoryModal.value = false;
    
    // 重新获取分类列表
    await fetchCategories();
  } catch (err) {
    console.error('更新分类失败:', err);
    alert('更新分类失败，请稍后重试');
  } finally {
    submitting.value = false;
  }
}

// 删除分类
function confirmDeleteCategory(category) {
  categoryToDelete.value = category;
  showDeleteCategoryModal.value = true;
}

async function deleteCategory() {
  if (!categoryToDelete.value) return;
  
  submitting.value = true;
  
  try {
    await api.product.categories.delete(categoryToDelete.value.category_id);
    
    showDeleteCategoryModal.value = false;
    categoryToDelete.value = null;
    
    // 重新获取分类列表和产品列表
    await Promise.all([fetchCategories(), fetchProducts()]);
  } catch (err) {
    console.error('删除分类失败:', err);
    alert('删除分类失败，请稍后重试');
  } finally {
    submitting.value = false;
  }
}

// 添加产品
const newProduct = reactive({
  name: '',
  category_id: '',
  sku: '',
  unit: '个',
  price: '',
  inventory_qty: 0,
  reorder_point: 0,
  status: 'ACTIVE'
});

async function addProduct() {
  // 表单验证
  if (!newProduct.name || !newProduct.price || !newProduct.unit) {
    alert('请填写必要信息');
    return;
  }
  
  submitting.value = true;
  
  try {
    await api.product.products.create({
      name: newProduct.name,
      category_id: newProduct.category_id || null,
      sku: newProduct.sku || null,
      unit: newProduct.unit,
      price: parseFloat(newProduct.price),
      inventory_qty: parseFloat(newProduct.inventory_qty) || 0,
      reorder_point: parseFloat(newProduct.reorder_point) || 0,
      status: newProduct.status
    });
    
    // 重置表单并关闭模态框
    Object.assign(newProduct, {
      name: '',
      category_id: '',
      sku: '',
      unit: '个',
      price: '',
      inventory_qty: 0,
      reorder_point: 0,
      status: 'ACTIVE'
    });
    
    showAddProductModal.value = false;
    
    // 重新获取产品列表
    await fetchProducts();
  } catch (err) {
    console.error('添加产品失败:', err);
    alert('添加产品失败，请稍后重试');
  } finally {
    submitting.value = false;
  }
}

// 编辑产品
const editingProduct = reactive({
  product_id: null,
  name: '',
  category_id: '',
  sku: '',
  unit: '',
  price: '',
  inventory_qty: 0,
  reorder_point: 0,
  status: ''
});

function editProduct(product) {
  console.log('编辑产品，原始数据:', product);
  editingProduct.product_id = product.product_id;
  editingProduct.name = product.name || '';
  
  // 修复category_id的赋值
  if (product.category) {
    // 如果category是数字ID
    if (typeof product.category === 'number') {
  editingProduct.category_id = product.category;
      console.log('分类是数字ID:', product.category);
    } 
    // 如果category是对象
    else if (typeof product.category === 'object' && product.category !== null) {
      editingProduct.category_id = product.category.category_id;
      console.log('分类是对象:', product.category, '设置ID为:', product.category.category_id);
    } 
    // 其他情况
    else {
      editingProduct.category_id = product.category;
      console.log('分类是其他类型:', typeof product.category, product.category);
    }
  } else {
    editingProduct.category_id = '';
    console.log('产品没有分类信息');
  }
  
  console.log('设置category_id为:', editingProduct.category_id);
  
  editingProduct.sku = product.sku || '';
  editingProduct.unit = product.unit || '个';
  editingProduct.price = product.price || 0;
  editingProduct.inventory_qty = product.inventory_qty || 0;
  editingProduct.reorder_point = product.reorder_point || 0;
  editingProduct.status = product.status || 'ACTIVE';
  
  // 打印所有可用的分类
  console.log('可用的分类列表:', categories.value);
  
  showEditProductModal.value = true;
}

async function updateProduct() {
  // 表单验证
  if (!editingProduct.name || !editingProduct.price || !editingProduct.unit) {
    alert('请填写必要信息');
    return;
  }
  
  submitting.value = true;
  console.log('准备更新产品，数据:', editingProduct);
  
  try {
    // 准备要发送的数据
    const updateData = {
      name: editingProduct.name,
      sku: editingProduct.sku || null,
      unit: editingProduct.unit,
      price: parseFloat(editingProduct.price),
      inventory_qty: parseFloat(editingProduct.inventory_qty) || 0,
      reorder_point: parseFloat(editingProduct.reorder_point) || 0,
      status: editingProduct.status
    };
    
    // 特别处理category_id
    if (editingProduct.category_id === '' || editingProduct.category_id === null) {
      updateData.category = null;
    } else {
      updateData.category = parseInt(editingProduct.category_id);
    }
    
    console.log('发送更新请求，数据:', updateData);
    const response = await api.product.products.update(editingProduct.product_id, updateData);
    console.log('更新产品成功，响应:', response);
    
    showEditProductModal.value = false;
    
    // 重新获取产品列表
    await fetchProducts();
  } catch (err) {
    console.error('更新产品失败:', err);
    if (err.response) {
      console.error('错误响应:', err.response.data);
      alert(`更新产品失败: ${JSON.stringify(err.response.data)}`);
    } else {
    alert('更新产品失败，请稍后重试');
    }
  } finally {
    submitting.value = false;
  }
}

// 初始化
onMounted(async () => {
  console.log('产品管理页面已加载');
  console.log('开始获取数据...');
  try {
    const [productsResponse, categoriesResponse] = await Promise.all([
      api.product.products.getAll(),
      api.product.categories.getAll()
    ]);
    console.log('获取到产品数据:', productsResponse);
    console.log('获取到分类数据:', categoriesResponse);
    
    // 检查数据结构
    if (Array.isArray(productsResponse)) {
    products.value = productsResponse;
      console.log('产品数据是数组，长度:', productsResponse.length);
      if (productsResponse.length > 0) {
        console.log('第一个产品示例:', JSON.stringify(productsResponse[0]));
        // 检查产品的分类字段
        const firstProduct = productsResponse[0];
        if (firstProduct.category) {
          console.log('产品分类字段类型:', typeof firstProduct.category);
          console.log('产品分类字段值:', firstProduct.category);
        }
      }
    } else {
      console.error('产品数据不是数组:', typeof productsResponse);
      products.value = [];
    }
    
    if (Array.isArray(categoriesResponse)) {
    categories.value = categoriesResponse;
      console.log('分类数据是数组，长度:', categoriesResponse.length);
      if (categoriesResponse.length > 0) {
        console.log('第一个分类示例:', JSON.stringify(categoriesResponse[0]));
      }
      
      // 创建分类ID到名称的映射
      console.log('创建分类映射:');
      categoriesResponse.forEach(category => {
        console.log(`分类ID: ${category.category_id}, 名称: ${category.name}`);
      });
    } else {
      console.error('分类数据不是数组:', typeof categoriesResponse);
      categories.value = [];
    }
    
    console.log('数据加载完成，当前选项卡:', activeTab.value);
  } catch (err) {
    console.error('数据加载失败:', err);
    error.value = '获取数据失败，请稍后重试';
  } finally {
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

.header-buttons {
  display: flex;
  gap: 12px;
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 1.25em;
  color: var(--primary-text-color, #121714);
  margin: 0;
}

.add-btn {
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

.tabs {
  display: flex;
  gap: 32px;
  padding: 0 16px;
  border-bottom: 1px solid var(--border-color, #DBE5DE);
  width: 100%;
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

.product-table-container, .category-container {
  padding: 0 16px 16px;
  width: 100%;
  overflow-x: auto;
}

.product-table, .category-table {
  width: 100%;
  border-collapse: collapse;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
  overflow: hidden;
}

.product-table th,
.product-table td,
.category-table th,
.category-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
  border-bottom: 1px solid var(--border-color, #DBE5DE);
}

.product-table th,
.category-table th {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.product-table td,
.category-table td {
  font-weight: 400;
  color: var(--primary-text-color, #121714);
}

.th-name, .td-name {
  min-width: 200px;
}

.th-category, .td-category,
.th-stock, .td-stock,
.th-price, .td-price,
.th-status, .td-status,
.th-action, .td-action,
.th-order, .td-order {
  text-align: center;
  min-width: 100px;
}

.td-category, .td-stock, .td-price, .td-order {
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

.edit-link, .delete-link {
  color: var(--secondary-text-color, #638770);
  font-weight: 700;
  cursor: pointer;
  margin: 0 5px;
}

.delete-link {
  color: #e53935;
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
.form-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 8px;
  font-size: 14px;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.warning-text {
  color: #e53935;
  font-size: 14px;
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

.delete-btn {
  background-color: #e53935;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 500;
  font-size: 14px;
  color: white;
  cursor: pointer;
}

.submit-btn:disabled, .delete-btn:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .product-table, .category-table {
    display: block;
    overflow-x: auto;
  }
  
  .product-table th, .category-table th {
    white-space: nowrap;
  }
}

/* 修复页面宽度超过1024px的问题 */
@media (min-width: 1024px) {
  .page-content-container {
    width: 100%;
    max-width: 100%;
  }
  
  .product-table-container, .category-container {
    width: 100%;
  }
  
  .product-table, .category-table {
    width: 100%;
  }
}
</style> 