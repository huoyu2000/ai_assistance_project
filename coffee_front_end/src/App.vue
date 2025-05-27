<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const currentUser = computed(() => authStore.user)
const isAuthenticated = computed(() => authStore.isAuthenticated)

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}

onMounted(() => {
  // 如果已登录，获取用户信息
  if (isAuthenticated.value) {
    authStore.fetchCurrentUser()
  }
})
</script>

<template>
  <!-- 登录页不显示侧边栏和顶部导航 -->
  <div v-if="$route.path === '/login'" class="login-page">
    <RouterView />
  </div>
  
  <!-- 已登录状态显示完整布局 -->
  <div v-else class="app-container">
    <aside class="sidebar">
      <nav class="main-nav">
        <RouterLink to="/" class="nav-link" :class="{ active: $route.path === '/' }">
          <div class="nav-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
          </div>
          <span>首页</span>
        </RouterLink>
        <RouterLink to="/product" class="nav-link" :class="{ active: $route.path.includes('/product') }">
          <div class="nav-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M18 8h1a4 4 0 0 1 0 8h-1"></path>
              <path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path>
              <line x1="6" y1="1" x2="6" y2="4"></line>
              <line x1="10" y1="1" x2="10" y2="4"></line>
              <line x1="14" y1="1" x2="14" y2="4"></line>
            </svg>
          </div>
          <span>商品</span>
        </RouterLink>
        <RouterLink to="/procurement" class="nav-link" :class="{ active: $route.path.includes('/procurement') }">
          <div class="nav-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="9" cy="21" r="1"></circle>
              <circle cx="20" cy="21" r="1"></circle>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>
          </div>
          <span>采购</span>
        </RouterLink>
        <RouterLink to="/sales" class="nav-link" :class="{ active: $route.path.includes('/sales') }">
          <div class="nav-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="12" y1="1" x2="12" y2="23"></line>
              <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
            </svg>
          </div>
          <span>销售</span>
        </RouterLink>
        <RouterLink to="/inventory" class="nav-link" :class="{ active: $route.path.includes('/inventory') }">
          <div class="nav-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
              <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
              <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>
          </div>
          <span>库存</span>
        </RouterLink>
        <RouterLink to="/finance" class="nav-link" :class="{ active: $route.path.includes('/finance') }">
          <div class="nav-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect>
              <line x1="16" y1="2" x2="16" y2="6"></line>
              <line x1="8" y1="2" x2="8" y2="6"></line>
              <line x1="3" y1="10" x2="21" y2="10"></line>
            </svg>
          </div>
          <span>财务</span>
        </RouterLink>
        <RouterLink to="/authority" class="nav-link" :class="{ active: $route.path.includes('/authority') }">
          <div class="nav-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="7" r="4"></circle>
              <path d="M5 22v-5c0-1.1.9-2 2-2h10a2 2 0 0 1 2 2v5"></path>
              <path d="M15 11h3a2 2 0 0 1 2 2v2a2 2 0 0 1-2 2h-3"></path>
            </svg>
          </div>
          <span>权限</span>
        </RouterLink>
      </nav>
    </aside>

    <div class="main-wrapper">
      <header class="top-header">
        <div class="header-content">
          <span class="header-title">咖啡店管理系统</span>
          <div class="user-info">
            <span class="user-name">{{ currentUser?.full_name || currentUser?.username || '用户' }}</span>
            <div class="user-menu">
            <div class="user-avatar">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              </div>
              <div class="dropdown-menu">
                <button class="dropdown-item" @click="handleLogout">退出登录</button>
              </div>
            </div>
          </div>
        </div>
      </header>
      
      <main class="main-content">
        <RouterView />
      </main>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

:root {
  --sidebar-width: 180px;
  --top-header-height: 64px;
  --primary-text-color: #121714;
  --secondary-text-color: #638770;
  --sidebar-bg: #F5F5F5;
  --sidebar-text-color: #121714;
  --sidebar-text-hover-color: #121714;
  --sidebar-active-bg: #F0F5F2;
  --sidebar-active-color: #121714;
  --main-bg-color: #F5F5F5;
  --content-bg-color: #FFFFFF;
  --border-color: #E5E8EB;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Space Grotesk', sans-serif;
}

body {
  color: var(--primary-text-color);
  background-color: var(--main-bg-color);
  overflow-x: hidden;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

.login-page {
  width: 100%;
  height: 100vh;
}

.app-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
  position: relative;
}

.sidebar {
  width: var(--sidebar-width);
  min-width: var(--sidebar-width);
  background-color: var(--sidebar-bg);
  color: var(--sidebar-text-color);
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  padding-top: 60px;
}

.main-nav {
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  color: var(--sidebar-text-color);
  text-decoration: none;
  transition: all 0.2s ease-in-out;
  font-weight: 500;
  font-size: 16px;
  gap: 16px;
}

.nav-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
}

.nav-link:hover {
  background-color: rgba(240, 245, 242, 0.5);
}

.nav-link.active {
  background-color: var(--sidebar-active-bg);
  color: var(--sidebar-active-color);
  font-weight: 500;
  border-left: 3px solid var(--secondary-text-color);
}

.main-wrapper {
  margin-left: var(--sidebar-width);
  width: calc(100% - var(--sidebar-width));
  max-width: calc(100% - var(--sidebar-width));
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.top-header {
  height: var(--top-header-height);
  width: 100%;
  background-color: white;
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 24px;
}

.header-title {
  font-size: 18px;
  font-weight: 500;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-name {
  font-size: 14px;
  font-weight: 500;
}

.user-menu {
  position: relative;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: var(--sidebar-active-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  background-color: white;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  width: 120px;
  display: none;
  z-index: 1000;
}

.user-menu:hover .dropdown-menu {
  display: block;
}

.dropdown-item {
  padding: 8px 16px;
  width: 100%;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 14px;
}

.dropdown-item:hover {
  background-color: var(--sidebar-active-bg);
}

.main-content {
  flex-grow: 1;
  padding: 24px;
  background-color: var(--main-bg-color);
}
</style>
