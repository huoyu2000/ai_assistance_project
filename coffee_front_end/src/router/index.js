import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import ProcurementManagement from '../views/ProcurementManagement.vue'
import SupplierDetail from '../views/SupplierDetail.vue'
import PurchaseOrderList from '../views/PurchaseOrderList.vue'
import PurchaseOrderDetail from '../views/PurchaseOrderDetail.vue'
import PurchaseOrderCreate from '../views/PurchaseOrderCreate.vue'
import OrdersManagement from '../views/OrdersManagement.vue'
import CustomersManagement from '../views/CustomersManagement.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false }
    },
    {
      path: '/',
      name: 'home',
      component: HomeView,
      meta: { requiresAuth: true }
    },
    {
      path: '/orders',
      name: 'orders',
      component: OrdersManagement,
      meta: { requiresAuth: true }
    },
    {
      path: '/orders/:id',
      name: 'order-detail',
      component: () => import('../views/OrderDetail.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/customers',
      name: 'customers',
      component: CustomersManagement,
      meta: { requiresAuth: true }
    },
    {
      path: '/customers/:id/orders',
      name: 'customer-orders',
      component: () => import('../views/CustomerOrders.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/product',
      name: 'product',
      component: () => import('../views/ProductManagement.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/inventory',
      name: 'inventory',
      component: () => import('../views/InventoryManagement.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/reports',
      name: 'reports',
      component: () => import('../views/ReportsManagement.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/procurement',
      name: 'procurement',
      component: ProcurementManagement,
      meta: { requiresAuth: true }
    },
    {
      path: '/procurement/supplier/:id',
      name: 'supplier-detail',
      component: SupplierDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/procurement/orders',
      name: 'purchase-orders',
      component: PurchaseOrderList,
      meta: { requiresAuth: true }
    },
    {
      path: '/procurement/orders/:id',
      name: 'purchase-order-detail',
      component: PurchaseOrderDetail,
      meta: { requiresAuth: true }
    },
    {
      path: '/procurement/orders/create',
      name: 'purchase-order-create',
      component: PurchaseOrderCreate,
      meta: { requiresAuth: true }
    },
    {
      path: '/procurement/add-supplier',
      name: 'add-supplier',
      component: () => import('../views/AddSupplier.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/sales',
      name: 'sales',
      component: () => import('../views/SalesManagement.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/finance',
      name: 'finance',
      component: () => import('../views/FinanceManagement.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/authority',
      name: 'authority',
      component: () => import('../views/AuthorityManagement.vue'),
      meta: { requiresAuth: true }
    },
  ],
})

// 路由守卫
router.beforeEach((to, from, next) => {
  // 检查路由是否需要认证
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth !== false);
  
  // 获取token
  const token = localStorage.getItem('token');
  
  if (requiresAuth && !token) {
    // 需要认证但没有token，重定向到登录页
    next('/login');
  } else if (to.path === '/login' && token) {
    // 已经登录，但访问登录页，重定向到首页
    next('/');
  } else {
    // 其他情况正常导航
    next();
  }
});

export default router
