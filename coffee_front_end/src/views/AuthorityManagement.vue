<template>
  <div class="page-content-container">
    <div class="header">
      <h1 class="page-title">权限管理</h1>
      <p class="page-description">管理系统用户、角色和权限配置。</p>
    </div>

    <!-- 角色管理部分 -->
    <div class="section-container">
      <h2 class="section-title">角色管理</h2>
      
      <!-- 加载状态 -->
      <div v-if="loading.roles" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <!-- 错误提示 -->
      <div v-else-if="error.roles" class="error-message">
        <p>{{ error.roles }}</p>
        <button @click="fetchRoles" class="retry-button">重试</button>
      </div>
      
      <div v-else>
        <div class="table-container">
          <table class="roles-table">
            <thead>
              <tr>
                <th>角色名称</th>
                <th>描述</th>
                <th>用户数量</th>
                <th>创建时间</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(role, index) in roles" :key="index">
                <td>{{ role.name }}</td>
                <td class="text-secondary">{{ role.description }}</td>
                <td class="text-secondary text-center">{{ role.userCount || 0 }}</td>
                <td class="text-secondary">{{ role.created_at }}</td>
                <td>
                  <div class="action-buttons">
                    <button class="btn btn-edit" @click="editRole(role)">编辑</button>
                    <button class="btn btn-delete" v-if="role.name !== '系统管理员'" @click="deleteRole(role)">删除</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="actions-container">
          <button class="btn btn-primary" @click="showAddRoleModal = true">
            <span class="btn-icon">+</span>
            <span>添加角色</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 权限配置部分 -->
    <div class="section-container">
      <h2 class="section-title">权限配置</h2>
      
      <!-- 加载状态 -->
      <div v-if="loading.permissions" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <!-- 错误提示 -->
      <div v-else-if="error.permissions" class="error-message">
        <p>{{ error.permissions }}</p>
        <button @click="handleRoleChange" class="retry-button">重试</button>
      </div>
      
      <div v-else class="permissions-container">
        <div class="role-selector">
          <label for="role-select">选择角色:</label>
          <select id="role-select" v-model="selectedRole" @change="handleRoleChange">
            <option v-for="role in roles" :key="role.name" :value="role.name">{{ role.name }}</option>
          </select>
        </div>
        
        <div class="permissions-grid">
          <div v-for="(module, moduleIndex) in permissionModules" :key="moduleIndex" class="permission-module">
            <div class="module-header">
              <label class="checkbox-container">
                <input type="checkbox" :checked="isModuleSelected(module)" @change="toggleModule(module)">
                <span class="checkmark"></span>
                <span class="module-name">{{ module.name }}</span>
              </label>
            </div>
            <div class="module-permissions">
              <div v-for="(perm, permIndex) in module.permissions" :key="permIndex" class="permission-item">
                <label class="checkbox-container">
                  <input type="checkbox" v-model="perm.granted">
                  <span class="checkmark"></span>
                  <span class="permission-name">{{ perm.name }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>
        
        <div class="actions-container">
          <button class="btn btn-primary" @click="savePermissions">保存配置</button>
          <button class="btn btn-secondary" @click="resetPermissions">重置</button>
        </div>
      </div>
    </div>

    <!-- 用户管理部分 -->
    <div class="section-container">
      <h2 class="section-title">用户管理</h2>
      
      <!-- 加载状态 -->
      <div v-if="loading.users" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <!-- 错误提示 -->
      <div v-else-if="error.users" class="error-message">
        <p>{{ error.users }}</p>
        <button @click="fetchUsers" class="retry-button">重试</button>
      </div>
      
      <div v-else>
        <div class="search-container">
          <input type="text" placeholder="搜索用户名或姓名..." class="search-input" v-model="userSearchQuery">
          <button class="btn btn-search">搜索</button>
        </div>
        
        <div class="table-container">
          <table class="users-table">
            <thead>
              <tr>
                <th>用户名</th>
                <th>姓名</th>
                <th>角色</th>
                <th>邮箱</th>
                <th>状态</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(user, index) in filteredUsers" :key="index">
                <td>{{ user.username }}</td>
                <td>{{ user.fullName || user.full_name }}</td>
                <td class="text-secondary">{{ user.role }}</td>
                <td class="text-secondary">{{ user.email }}</td>
                <td>
                  <span class="status-badge" :class="{ 'inactive': user.status !== '激活' }">
                    {{ user.status }}
                  </span>
                </td>
                <td>
                  <div class="action-buttons">
                    <button class="btn btn-edit" @click="editUser(user)">编辑</button>
                    <button class="btn btn-reset" @click="showResetPasswordDialog(user)">重置密码</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="actions-container">
          <button class="btn btn-primary" @click="showAddUserModal = true">
            <span class="btn-icon">+</span>
            <span>添加用户</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 操作日志部分 -->
    <div class="section-container">
      <h2 class="section-title">操作日志</h2>
      
      <div class="log-filters">
        <div class="filter-group">
          <label>操作日期:</label>
          <div class="date-range">
            <input type="date" class="date-input" v-model="logFilters.startDate">
            <span>至</span>
            <input type="date" class="date-input" v-model="logFilters.endDate">
          </div>
        </div>
        
        <div class="filter-group">
          <label>操作类型:</label>
          <select v-model="logFilters.actionType">
            <option value="">全部</option>
            <option value="LOGIN">登录</option>
            <option value="CREATE">创建</option>
            <option value="UPDATE">修改</option>
            <option value="DELETE">删除</option>
          </select>
        </div>
        
        <div class="filter-group">
          <label>操作人:</label>
          <input type="text" v-model="logFilters.operator" placeholder="输入操作人">
        </div>
        
        <button class="btn btn-search" @click="filterLogs">筛选</button>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="loading.logs" class="loading-container">
        <div class="loading-spinner"></div>
        <p>加载中...</p>
      </div>
      
      <!-- 错误提示 -->
      <div v-else-if="error.logs" class="error-message">
        <p>{{ error.logs }}</p>
        <button @click="fetchOperationLogs" class="retry-button">重试</button>
      </div>
      
      <div v-else>
        <div class="table-container">
          <table class="logs-table">
            <thead>
              <tr>
                <th>时间</th>
                <th>操作人</th>
                <th>IP地址</th>
                <th>操作类型</th>
                <th>操作详情</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(log, index) in operationLogs" :key="index">
                <td>{{ log.timestamp }}</td>
                <td>{{ log.operator }}</td>
                <td class="text-secondary">{{ log.ipAddress }}</td>
                <td>
                  <span class="action-type" :class="log.actionType">{{ log.actionTypeName }}</span>
                </td>
                <td class="text-secondary log-detail">{{ log.detail }}</td>
              </tr>
            </tbody>
          </table>
        </div>
        
        <div class="pagination">
          <button class="pagination-btn" :disabled="currentPage === 1" @click="goToPage(currentPage - 1)">&lt;</button>
          <span class="pagination-info">第 {{ currentPage }} 页，共 {{ totalPages }} 页</span>
          <button class="pagination-btn" :disabled="currentPage === totalPages" @click="goToPage(currentPage + 1)">&gt;</button>
        </div>
      </div>
    </div>

    <!-- 添加角色模态框 -->
    <div class="modal-overlay" v-if="showAddRoleModal" @click.self="showAddRoleModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>添加角色</h3>
          <button class="close-btn" @click="showAddRoleModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="role-name">角色名称</label>
            <input type="text" id="role-name" v-model="newRole.name" placeholder="输入角色名称">
          </div>
          <div class="form-group">
            <label for="role-description">角色描述</label>
            <textarea id="role-description" v-model="newRole.description" placeholder="输入角色描述" rows="3"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showAddRoleModal = false">取消</button>
          <button class="submit-btn" @click="addRole">保存</button>
        </div>
      </div>
    </div>

    <!-- 编辑角色模态框 -->
    <div class="modal-overlay" v-if="showEditRoleModal" @click.self="showEditRoleModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>编辑角色</h3>
          <button class="close-btn" @click="showEditRoleModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="edit-role-name">角色名称</label>
            <input type="text" id="edit-role-name" v-model="editingRole.name" placeholder="输入角色名称">
          </div>
          <div class="form-group">
            <label for="edit-role-description">角色描述</label>
            <textarea id="edit-role-description" v-model="editingRole.description" placeholder="输入角色描述" rows="3"></textarea>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showEditRoleModal = false">取消</button>
          <button class="submit-btn" @click="updateRole">更新</button>
        </div>
      </div>
    </div>

    <!-- 添加用户模态框 -->
    <div class="modal-overlay" v-if="showAddUserModal" @click.self="showAddUserModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>添加用户</h3>
          <button class="close-btn" @click="showAddUserModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="user-username">用户名</label>
            <input type="text" id="user-username" v-model="newUser.username" placeholder="输入用户名">
          </div>
          <div class="form-group">
            <label for="user-fullname">姓名</label>
            <input type="text" id="user-fullname" v-model="newUser.fullName" placeholder="输入姓名">
          </div>
          <div class="form-group">
            <label for="user-role">角色</label>
            <select id="user-role" v-model="newUser.role">
              <option value="">选择角色</option>
              <option v-for="role in roles" :key="role.name" :value="role.name">{{ role.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="user-email">邮箱</label>
            <input type="email" id="user-email" v-model="newUser.email" placeholder="输入邮箱">
          </div>
          <div class="form-group">
            <label for="user-password">密码</label>
            <input type="password" id="user-password" v-model="newUser.password" placeholder="输入密码">
          </div>
          <div class="form-group">
            <label for="user-status">状态</label>
            <select id="user-status" v-model="newUser.status">
              <option value="ACTIVE">激活</option>
              <option value="DISABLED">停用</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showAddUserModal = false">取消</button>
          <button class="submit-btn" @click="addUser">保存</button>
        </div>
      </div>
    </div>

    <!-- 编辑用户模态框 -->
    <div class="modal-overlay" v-if="showEditUserModal" @click.self="showEditUserModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>编辑用户</h3>
          <button class="close-btn" @click="showEditUserModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="edit-user-username">用户名</label>
            <input type="text" id="edit-user-username" v-model="editingUser.username" disabled>
          </div>
          <div class="form-group">
            <label for="edit-user-fullname">姓名</label>
            <input type="text" id="edit-user-fullname" v-model="editingUser.fullName" placeholder="输入姓名">
          </div>
          <div class="form-group">
            <label for="edit-user-role">角色</label>
            <select id="edit-user-role" v-model="editingUser.role">
              <option value="">无角色</option>
              <option v-for="role in roles" :key="role.name" :value="role.name">{{ role.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="edit-user-email">邮箱</label>
            <input type="email" id="edit-user-email" v-model="editingUser.email" placeholder="输入邮箱">
          </div>
          <div class="form-group">
            <label for="edit-user-status">状态</label>
            <select id="edit-user-status" v-model="editingUser.status">
              <option value="ACTIVE">激活</option>
              <option value="DISABLED">停用</option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showEditUserModal = false">取消</button>
          <button class="submit-btn" @click="updateUser">更新</button>
        </div>
      </div>
    </div>

    <!-- 重置密码模态框 -->
    <div class="modal-overlay" v-if="showResetPasswordModal" @click.self="showResetPasswordModal = false">
      <div class="modal-container">
        <div class="modal-header">
          <h3>重置密码</h3>
          <button class="close-btn" @click="showResetPasswordModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>用户</label>
            <p class="info-text">{{ resetPasswordUser.fullName }} ({{ resetPasswordUser.username }})</p>
          </div>
          <div class="form-group">
            <label for="new-password">新密码</label>
            <input type="password" id="new-password" v-model="newPassword" placeholder="输入新密码">
          </div>
          <div class="form-group">
            <label for="confirm-password">确认密码</label>
            <input type="password" id="confirm-password" v-model="confirmPassword" placeholder="再次输入新密码">
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-btn" @click="showResetPasswordModal = false">取消</button>
          <button class="submit-btn" @click="resetPassword">确认重置</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from 'vue';
import api from '../api/api';

// 状态变量
const loading = ref({
  roles: false,
  permissions: false,
  users: false,
  logs: false
});
const error = ref({
  roles: null,
  permissions: null,
  users: null,
  logs: null
});

// 角色数据
const roles = ref([]);

// 权限模块
const permissionModules = ref([
  {
    name: '商品管理',
    permissions: [
      { id: 'product_view', name: '查看', granted: false },
      { id: 'product_add', name: '添加', granted: false },
      { id: 'product_edit', name: '编辑', granted: false },
      { id: 'product_delete', name: '删除', granted: false }
    ]
  },
  {
    name: '采购管理',
    permissions: [
      { id: 'procurement_view', name: '查看', granted: false },
      { id: 'procurement_add', name: '添加', granted: false },
      { id: 'procurement_edit', name: '编辑', granted: false },
      { id: 'procurement_delete', name: '删除', granted: false }
    ]
  },
  {
    name: '销售管理',
    permissions: [
      { id: 'sales_view', name: '查看', granted: false },
      { id: 'sales_add', name: '添加', granted: false },
      { id: 'sales_refund', name: '退款', granted: false }
    ]
  },
  {
    name: '库存管理',
    permissions: [
      { id: 'inventory_view', name: '查看', granted: false },
      { id: 'inventory_add', name: '入库', granted: false },
      { id: 'inventory_out', name: '出库', granted: false },
      { id: 'inventory_adjust', name: '调整', granted: false }
    ]
  },
  {
    name: '财务管理',
    permissions: [
      { id: 'finance_view', name: '查看', granted: false },
      { id: 'finance_daily', name: '日结', granted: false },
      { id: 'finance_export', name: '导出', granted: false }
    ]
  },
  {
    name: '权限管理',
    permissions: [
      { id: 'auth_view', name: '查看', granted: false },
      { id: 'auth_role', name: '角色管理', granted: false },
      { id: 'auth_user', name: '用户管理', granted: false },
      { id: 'auth_perm', name: '权限配置', granted: false }
    ]
  }
]);

// 用户数据
const users = ref([]);

// 操作日志数据
const operationLogs = ref([]);

// 选中的角色
const selectedRole = ref('');

// 日志筛选条件
const logFilters = ref({
  startDate: '',
  endDate: '',
  actionType: '',
  operator: ''
});

// 分页
const currentPage = ref(1);
const totalPages = ref(1);
const pageSize = ref(10);

// 添加角色模态框
const showAddRoleModal = ref(false);
const newRole = reactive({
  name: '',
  description: '',
});

// 编辑角色模态框
const showEditRoleModal = ref(false);
const editingRole = reactive({
  role_id: null,
  name: '',
  description: '',
});

// 添加用户模态框
const showAddUserModal = ref(false);
const newUser = reactive({
  username: '',
  fullName: '',
  role: '',
  email: '',
  password: '',
  status: 'ACTIVE'
});

// 编辑用户模态框
const showEditUserModal = ref(false);
const editingUser = reactive({
  user_id: null,
  username: '',
  fullName: '',
  role: '',
  email: '',
  status: 'ACTIVE'
});

// 重置密码模态框
const showResetPasswordModal = ref(false);
const resetPasswordUser = reactive({
  user_id: null,
  username: '',
  fullName: ''
});
const newPassword = ref('');
const confirmPassword = ref('');

// 用户搜索
const userSearchQuery = ref('');
const filteredUsers = computed(() => {
  if (!userSearchQuery.value) {
    return users.value;
  }
  
  const query = userSearchQuery.value.toLowerCase();
  return users.value.filter(user => 
    user.username.toLowerCase().includes(query) || 
    user.full_name.toLowerCase().includes(query)
  );
});

// 获取角色列表
async function fetchRoles() {
  loading.value.roles = true;
  error.value.roles = null;
  
  try {
    const response = await api.auth.roles.getAll();
    console.log('获取到的角色数据:', response);
    
    // 处理分页格式的响应
    if (response && response.results) {
      roles.value = response.results.map(role => ({
        ...role,
        userCount: role.userCount || 0 // 确保userCount字段存在
      }));
    } else if (Array.isArray(response)) {
      roles.value = response.map(role => ({
        ...role,
        userCount: role.userCount || 0 // 确保userCount字段存在
      }));
    } else {
      roles.value = [];
    }
    
    // 如果有角色，默认选中第一个
    if (roles.value.length > 0) {
      selectedRole.value = roles.value[0].name;
      await fetchRolePermissions(roles.value[0].role_id);
    }
  } catch (err) {
    console.error('获取角色列表失败:', err);
    error.value.roles = '获取角色列表失败，请稍后重试';
    
    // 使用模拟数据
    roles.value = [
      { 
        role_id: 1,
        name: '系统管理员', 
        description: '拥有系统所有权限', 
        userCount: 1, 
        created_at: '2023-10-01' 
      },
      { 
        role_id: 2,
        name: '店长', 
        description: '管理门店日常运营，包括销售、库存、人员等', 
        userCount: 2, 
        created_at: '2023-10-01' 
      },
      { 
        role_id: 3,
        name: '值班经理', 
        description: '代理店长职责，负责日常事务管理', 
        userCount: 3, 
        created_at: '2023-10-05' 
      },
      { 
        role_id: 4,
        name: '咖啡师', 
        description: '制作咖啡饮品，维护咖啡设备', 
        userCount: 5, 
        created_at: '2023-10-10' 
      },
      { 
        role_id: 5,
        name: '收银员', 
        description: '负责前台收银、顾客接待', 
        userCount: 4, 
        created_at: '2023-10-15' 
      }
    ];
    
    // 设置默认选中角色
    selectedRole.value = '店长';
  } finally {
    loading.value.roles = false;
  }
}

// 获取角色权限
async function fetchRolePermissions(roleId) {
  loading.value.permissions = true;
  error.value.permissions = null;
  
  try {
    console.log('获取角色权限，角色ID:', roleId);
    const response = await api.auth.roles.getPermissions(roleId);
    console.log('获取到的权限数据:', response);
    
    // 重置所有权限
    permissionModules.value.forEach(module => {
      module.permissions.forEach(perm => {
        perm.granted = false;
      });
    });
    
    // 设置角色拥有的权限
    if (response && Array.isArray(response)) {
      response.forEach(rolePerm => {
        const permCode = rolePerm.permission_code;
        console.log('权限代码:', permCode);
        
        permissionModules.value.forEach(module => {
          module.permissions.forEach(perm => {
            if (perm.id === permCode) {
              console.log('匹配到权限:', perm.id);
              perm.granted = true;
            }
          });
        });
      });
    }
  } catch (err) {
    console.error('获取角色权限失败:', err);
    error.value.permissions = '获取角色权限失败，请稍后重试';
  } finally {
    loading.value.permissions = false;
  }
}

// 获取用户列表
async function fetchUsers() {
  loading.value.users = true;
  error.value.users = null;
  
  try {
    const response = await api.auth.staff.getAll();
    console.log('获取到的用户数据:', response);
    
    // 处理分页格式的响应
    let userData = [];
    if (response && response.results) {
      userData = response.results;
    } else {
      userData = response; // 兼容非分页格式
    }
    
    users.value = userData.map(user => ({
      ...user,
      fullName: user.full_name,
      role: user.role_name || '无角色',
      status: user.is_active ? '激活' : '停用'
    }));
  } catch (err) {
    console.error('获取用户列表失败:', err);
    error.value.users = '获取用户列表失败，请稍后重试';
    
    // 使用模拟数据
    users.value = [
      { 
        user_id: 1,
        username: 'admin', 
        fullName: '管理员', 
        role: '系统管理员', 
        email: 'admin@example.com', 
        status: '激活' 
      },
      { 
        user_id: 2,
        username: 'manager', 
        fullName: '张店长', 
        role: '店长', 
        email: 'manager@example.com', 
        status: '激活' 
      },
      { 
        user_id: 3,
        username: 'shift01', 
        fullName: '李经理', 
        role: '值班经理', 
        email: 'shift01@example.com', 
        status: '激活' 
      },
      { 
        user_id: 4,
        username: 'barista01', 
        fullName: '王咖啡', 
        role: '咖啡师', 
        email: 'barista01@example.com', 
        status: '激活' 
      },
      { 
        user_id: 5,
        username: 'barista02', 
        fullName: '赵咖啡', 
        role: '咖啡师', 
        email: 'barista02@example.com', 
        status: '停用' 
      }
    ];
  } finally {
    loading.value.users = false;
  }
}

// 获取操作日志
async function fetchOperationLogs() {
  loading.value.logs = true;
  error.value.logs = null;
  
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    };
    
    if (logFilters.value.startDate) {
      params.start_date = logFilters.value.startDate;
    }
    
    if (logFilters.value.endDate) {
      params.end_date = logFilters.value.endDate;
    }
    
    if (logFilters.value.actionType) {
      params.op_type = logFilters.value.actionType;
    }
    
    if (logFilters.value.operator) {
      params.operator = logFilters.value.operator;
    }
    
    const response = await api.auth.logs.getOperationLogs(params);
    
    if (response && response.results) {
      operationLogs.value = response.results.map(log => ({
        timestamp: formatDateTime(log.timestamp),
        operator: log.user_name || '未知',
        ipAddress: log.ip_addr,
        actionType: log.op_type.toLowerCase(),
        actionTypeName: getActionTypeName(log.op_type),
        detail: log.details
      }));
      
      totalPages.value = Math.ceil(response.count / pageSize.value);
    } else {
      operationLogs.value = [];
      totalPages.value = 1;
    }
  } catch (err) {
    console.error('获取操作日志失败:', err);
    error.value.logs = '获取操作日志失败，请稍后重试';
    
    // 使用模拟数据
    operationLogs.value = [
      { 
        timestamp: '2023-11-15 08:32:45', 
        operator: '张店长', 
        ipAddress: '192.168.1.101', 
        actionType: 'login', 
        actionTypeName: '登录', 
        detail: '用户登录系统' 
      },
      { 
        timestamp: '2023-11-15 09:15:22', 
        operator: '张店长', 
        ipAddress: '192.168.1.101', 
        actionType: 'create', 
        actionTypeName: '创建', 
        detail: '创建新商品：拿铁咖啡' 
      },
      { 
        timestamp: '2023-11-15 10:22:33', 
        operator: '李经理', 
        ipAddress: '192.168.1.102', 
        actionType: 'update', 
        actionTypeName: '修改', 
        detail: '修改商品价格：摩卡咖啡 $4.5 -> $4.8' 
      },
      { 
        timestamp: '2023-11-15 11:45:12', 
        operator: '钱仓管', 
        ipAddress: '192.168.1.105', 
        actionType: 'create', 
        actionTypeName: '创建', 
        detail: '创建采购单：20231115-001' 
      },
      { 
        timestamp: '2023-11-15 13:30:45', 
        operator: '孙收银', 
        ipAddress: '192.168.1.103', 
        actionType: 'create', 
        actionTypeName: '创建', 
        detail: '创建销售单：S20231115-042' 
      },
      { 
        timestamp: '2023-11-15 15:18:33', 
        operator: '管理员', 
        ipAddress: '192.168.1.100', 
        actionType: 'update', 
        actionTypeName: '修改', 
        detail: '修改用户角色：王咖啡 咖啡师 -> 值班经理' 
      },
      { 
        timestamp: '2023-11-15 16:22:51', 
        operator: '管理员', 
        ipAddress: '192.168.1.100', 
        actionType: 'delete', 
        actionTypeName: '删除', 
        detail: '删除过期商品：草莓蛋糕' 
      }
    ];
    totalPages.value = 1;
  } finally {
    loading.value.logs = false;
  }
}

// 格式化日期时间
function formatDateTime(dateTimeStr) {
  if (!dateTimeStr) return '';
  
  const date = new Date(dateTimeStr);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const hours = String(date.getHours()).padStart(2, '0');
  const minutes = String(date.getMinutes()).padStart(2, '0');
  const seconds = String(date.getSeconds()).padStart(2, '0');
  
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// 获取操作类型名称
function getActionTypeName(opType) {
  const typeMap = {
    'LOGIN': '登录',
    'CREATE': '创建',
    'UPDATE': '修改',
    'DELETE': '删除'
  };
  
  return typeMap[opType] || opType;
}

// 检查模块是否全选
function isModuleSelected(module) {
  return module.permissions.every(p => p.granted);
}

// 切换模块选择状态
function toggleModule(module) {
  const allSelected = isModuleSelected(module);
  module.permissions.forEach(p => {
    p.granted = !allSelected;
  });
}

// 角色管理功能
async function addRole() {
  if (!newRole.name || !newRole.description) {
    alert('请填写必要信息');
    return;
  }
  
  try {
    const response = await api.auth.roles.create({
      name: newRole.name,
      description: newRole.description
    });
    
    // 添加到角色列表
    roles.value.push(response);
    
    // 重置表单并关闭模态框
    Object.assign(newRole, {
      name: '',
      description: ''
    });
    
    showAddRoleModal.value = false;
  } catch (err) {
    console.error('创建角色失败:', err);
    alert('创建角色失败: ' + (err.response?.data?.detail || '未知错误'));
  }
}

async function editRole(role) {
  editingRole.role_id = role.role_id;
  editingRole.name = role.name;
  editingRole.description = role.description;
  
  showEditRoleModal.value = true;
}

async function updateRole() {
  if (!editingRole.name || !editingRole.description) {
    alert('请填写必要信息');
    return;
  }
  
  try {
    const response = await api.auth.roles.update(editingRole.role_id, {
      name: editingRole.name,
      description: editingRole.description
    });
    
    // 更新角色列表
    const index = roles.value.findIndex(r => r.role_id === editingRole.role_id);
    if (index !== -1) {
      roles.value[index] = response;
    }
    
    showEditRoleModal.value = false;
  } catch (err) {
    console.error('更新角色失败:', err);
    alert('更新角色失败: ' + (err.response?.data?.detail || '未知错误'));
  }
}

async function deleteRole(role) {
  if (role.name === '系统管理员') {
    alert('系统管理员角色不能删除');
    return;
  }
  
  if (confirm(`确定要删除角色 "${role.name}" 吗？`)) {
    try {
      await api.auth.roles.delete(role.role_id);
      
      // 从角色列表中移除
      const index = roles.value.findIndex(r => r.role_id === role.role_id);
      if (index !== -1) {
        roles.value.splice(index, 1);
      }
    } catch (err) {
      console.error('删除角色失败:', err);
      alert('删除角色失败: ' + (err.response?.data?.detail || '未知错误'));
    }
  }
}

// 权限配置功能
async function savePermissions() {
  if (!selectedRole.value) {
    alert('请先选择角色');
    return;
  }
  
  try {
    const role = roles.value.find(r => r.name === selectedRole.value);
    console.log('保存权限配置，角色:', role);
    if (!role) return;
    
    // 获取所有已授权的权限ID
    const grantedPermissions = [];
    permissionModules.value.forEach(module => {
      module.permissions.forEach(perm => {
        if (perm.granted) {
          grantedPermissions.push(perm.id);
        }
      });
    });
    console.log('已授权的权限:', grantedPermissions);
    
    // 获取角色当前的权限
    const currentPermissions = await api.auth.roles.getPermissions(role.role_id);
    console.log('当前权限:', currentPermissions);
    const currentPermIds = currentPermissions.map(p => p.permission_code);
    console.log('当前权限ID:', currentPermIds);
    
    // 需要添加的权限
    const toAdd = grantedPermissions.filter(id => !currentPermIds.includes(id));
    console.log('需要添加的权限:', toAdd);
    
    // 需要移除的权限
    const toRemove = currentPermIds.filter(id => !grantedPermissions.includes(id));
    console.log('需要移除的权限:', toRemove);
    
    // 批量添加权限
    for (const permId of toAdd) {
      console.log('添加权限:', permId);
      await api.auth.roles.addPermission(role.role_id, permId);
    }
    
    // 批量移除权限
    for (const permId of toRemove) {
      console.log('移除权限:', permId);
      await api.auth.roles.removePermission(role.role_id, permId);
    }
    
    alert('权限配置已保存');
  } catch (err) {
    console.error('保存权限配置失败:', err);
    alert('保存权限配置失败: ' + (err.response?.data?.detail || '未知错误'));
  }
}

async function resetPermissions() {
  if (confirm('确定要重置权限配置吗？所有更改将丢失。')) {
    const role = roles.value.find(r => r.name === selectedRole.value);
    if (role) {
      await fetchRolePermissions(role.role_id);
      alert('权限配置已重置');
    }
  }
}

// 用户管理功能
async function addUser() {
  if (!newUser.username || !newUser.fullName || !newUser.role || !newUser.email || !newUser.password) {
    alert('请填写必要信息');
    return;
  }
  
  try {
    const roleObj = roles.value.find(r => r.name === newUser.role);
    
    const response = await api.auth.staff.create({
      username: newUser.username,
      full_name: newUser.fullName,
      role: roleObj ? roleObj.role_id : null,
      email: newUser.email,
      password: newUser.password,
      status: newUser.status
    });
    
    // 添加到用户列表
    users.value.push({
      ...response,
      fullName: response.full_name,
      role: roleObj ? roleObj.name : '无角色',
      status: response.is_active ? '激活' : '停用'
    });
    
    // 重置表单并关闭模态框
    Object.assign(newUser, {
      username: '',
      fullName: '',
      role: '',
      email: '',
      password: '',
      status: 'ACTIVE'
    });
    
    showAddUserModal.value = false;
  } catch (err) {
    console.error('创建用户失败:', err);
    alert('创建用户失败: ' + (err.response?.data?.detail || '未知错误'));
  }
}

async function editUser(user) {
  editingUser.user_id = user.user_id;
  editingUser.username = user.username;
  editingUser.fullName = user.fullName || user.full_name;
  editingUser.role = user.role;
  editingUser.email = user.email;
  editingUser.status = user.status === '激活' ? 'ACTIVE' : 'DISABLED';
  
  showEditUserModal.value = true;
}

async function updateUser() {
  if (!editingUser.fullName || !editingUser.role || !editingUser.email) {
    alert('请填写必要信息');
    return;
  }
  
  try {
    const roleObj = roles.value.find(r => r.name === editingUser.role);
    
    const response = await api.auth.staff.update(editingUser.user_id, {
      full_name: editingUser.fullName,
      role: roleObj ? roleObj.role_id : null,
      email: editingUser.email,
      status: editingUser.status
    });
    
    // 更新用户列表
    const index = users.value.findIndex(u => u.user_id === editingUser.user_id);
    if (index !== -1) {
      users.value[index] = {
        ...response,
        fullName: response.full_name,
        role: roleObj ? roleObj.name : '无角色',
        status: response.is_active ? '激活' : '停用'
      };
    }
    
    showEditUserModal.value = false;
  } catch (err) {
    console.error('更新用户失败:', err);
    alert('更新用户失败: ' + (err.response?.data?.detail || '未知错误'));
  }
}

function showResetPasswordDialog(user) {
  resetPasswordUser.user_id = user.user_id;
  resetPasswordUser.username = user.username;
  resetPasswordUser.fullName = user.fullName || user.full_name;
  
  newPassword.value = '';
  confirmPassword.value = '';
  showResetPasswordModal.value = true;
}

async function resetPassword() {
  if (!newPassword.value) {
    alert('请输入新密码');
    return;
  }
  
  if (newPassword.value !== confirmPassword.value) {
    alert('两次输入的密码不一致');
    return;
  }
  
  try {
    await api.auth.staff.resetPassword(resetPasswordUser.user_id, newPassword.value);
    alert(`用户 ${resetPasswordUser.fullName} 的密码已重置`);
    showResetPasswordModal.value = false;
  } catch (err) {
    console.error('重置密码失败:', err);
    alert('重置密码失败: ' + (err.response?.data?.detail || '未知错误'));
  }
}

// 日志筛选功能
function filterLogs() {
  currentPage.value = 1;
  fetchOperationLogs();
}

function goToPage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
    fetchOperationLogs();
  }
}

// 监听选中角色变化
function handleRoleChange() {
  const role = roles.value.find(r => r.name === selectedRole.value);
  console.log('选择角色:', role);
  if (role) {
    fetchRolePermissions(role.role_id);
  }
}

// 初始化
onMounted(async () => {
  console.log('权限管理页面已加载');
  
  // 设置默认日期范围
  const today = new Date();
  const thirtyDaysAgo = new Date();
  thirtyDaysAgo.setDate(today.getDate() - 30);
  
  logFilters.value.startDate = thirtyDaysAgo.toISOString().split('T')[0];
  logFilters.value.endDate = today.toISOString().split('T')[0];
  
  // 并行加载数据
  await Promise.all([
    fetchRoles(),
    fetchUsers(),
    fetchOperationLogs()
  ]);
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
  padding: 16px;
  width: 100%;
}

.page-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 32px;
  line-height: 1.25em;
  color: var(--primary-text-color, #121714);
  margin: 0 0 12px 0;
}

.page-description {
  font-size: 14px;
  line-height: 1.5em;
  color: var(--secondary-text-color, #638770);
  margin: 0;
}

.section-container {
  padding: 0 16px 24px;
  width: 100%;
}

.section-title {
  font-family: 'Space Grotesk', sans-serif;
  font-weight: 700;
  font-size: 22px;
  line-height: 1.27em;
  color: var(--primary-text-color, #121714);
  margin: 20px 0 12px;
  padding: 0;
}

.table-container {
  width: 100%;
  overflow-x: auto;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
  margin-bottom: 16px;
}

.roles-table, .users-table, .logs-table {
  width: 100%;
  border-collapse: collapse;
}

.roles-table th, .roles-table td,
.users-table th, .users-table td,
.logs-table th, .logs-table td {
  padding: 12px 16px;
  text-align: left;
  font-size: 14px;
}

.roles-table th, .users-table th, .logs-table th {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  background-color: var(--content-bg-color, #FFFFFF);
}

.roles-table td, .users-table td, .logs-table td {
  border-top: 1px solid var(--border-color, #E5E8EB);
  height: 72px;
}

.text-secondary {
  color: var(--secondary-text-color, #638770);
}

.text-center {
  text-align: center;
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
  background-color: #FFECEC;
  color: #FF6B6B;
}

.action-type {
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.action-type.login {
  background-color: #E8F5FF;
  color: #1890FF;
}

.action-type.create {
  background-color: #F0F5F2;
  color: #52C41A;
}

.action-type.update {
  background-color: #FFF7E6;
  color: #FA8C16;
}

.action-type.delete {
  background-color: #FFF1F0;
  color: #FF4D4F;
}

.log-detail {
  max-width: 300px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.actions-container {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 16px;
}

.btn {
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.btn-primary {
  background-color: var(--primary-text-color, #121714);
  color: white;
}

.btn-secondary {
  background-color: var(--sidebar-active-bg, #F0F5F2);
  color: var(--primary-text-color, #121714);
}

.btn-edit {
  background-color: #E8F5FF;
  color: #1890FF;
}

.btn-delete {
  background-color: #FFF1F0;
  color: #FF4D4F;
}

.btn-reset {
  background-color: #FFF7E6;
  color: #FA8C16;
}

.btn-search {
  background-color: var(--primary-text-color, #121714);
  color: white;
}

.btn-icon {
  font-size: 16px;
  font-weight: 700;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

/* 权限配置样式 */
.permissions-container {
  padding: 16px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 12px;
}

.role-selector {
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.role-selector label {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
}

.role-selector select {
  padding: 8px 12px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 8px;
  background-color: var(--content-bg-color, #FFFFFF);
  font-size: 14px;
  min-width: 200px;
}

.permissions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.permission-module {
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 8px;
  overflow: hidden;
}

.module-header {
  padding: 12px 16px;
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border-bottom: 1px solid var(--border-color, #DBE5DE);
}

.module-name {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
}

.module-permissions {
  padding: 16px;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  position: relative;
  padding-left: 28px;
}

.checkbox-container input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}

.checkmark {
  position: absolute;
  left: 0;
  height: 18px;
  width: 18px;
  background-color: #FFFFFF;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 4px;
}

.checkbox-container:hover input ~ .checkmark {
  background-color: var(--sidebar-active-bg, #F0F5F2);
}

.checkbox-container input:checked ~ .checkmark {
  background-color: var(--primary-text-color, #121714);
  border-color: var(--primary-text-color, #121714);
}

.checkmark:after {
  content: "";
  position: absolute;
  display: none;
}

.checkbox-container input:checked ~ .checkmark:after {
  display: block;
}

.checkbox-container .checkmark:after {
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

/* 用户管理样式 */
.search-container {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.search-input {
  flex: 1;
  padding: 8px 16px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 8px;
  font-size: 14px;
}

/* 日志筛选样式 */
.log-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
  padding: 16px;
  background-color: var(--sidebar-active-bg, #F0F5F2);
  border-radius: 12px;
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-group label {
  font-weight: 500;
  color: var(--primary-text-color, #121714);
  white-space: nowrap;
}

.filter-group select,
.filter-group input {
  padding: 8px 12px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 8px;
  background-color: var(--content-bg-color, #FFFFFF);
  font-size: 14px;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 8px;
}

.date-input {
  width: 150px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 24px;
}

.pagination-btn {
  padding: 6px 12px;
  border: 1px solid var(--border-color, #DBE5DE);
  border-radius: 4px;
  background-color: var(--content-bg-color, #FFFFFF);
  cursor: pointer;
}

.pagination-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.pagination-info {
  font-size: 14px;
  color: var(--secondary-text-color, #638770);
}

/* 加载状态 */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
  width: 100%;
}

.loading-spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  border-top: 4px solid var(--primary-color, #38E078);
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* 错误消息 */
.error-message {
  background-color: #FFECEC;
  border-radius: 12px;
  padding: 16px;
  margin: 16px;
  color: #FF6B6B;
  text-align: center;
}

.retry-button {
  background-color: #FF6B6B;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  margin-top: 8px;
  cursor: pointer;
  font-weight: 500;
}

@media (max-width: 768px) {
  .permissions-grid {
    grid-template-columns: 1fr;
  }
  
  .module-permissions {
    grid-template-columns: 1fr;
  }
  
  .log-filters {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .filter-group {
    width: 100%;
  }
  
  .date-range {
    flex-direction: column;
    align-items: flex-start;
  }
}

/* 修复页面宽度超过1024px的问题 */
@media (min-width: 1024px) {
  .page-content-container {
    width: 100%;
    max-width: 100%;
  }
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
  resize: vertical;
  min-height: 80px;
}

.form-group .info-text {
  font-size: 14px;
  color: var(--secondary-text-color, #638770);
  margin: 4px 0;
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
</style> 