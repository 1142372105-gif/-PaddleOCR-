<template>
  <div class="layout">
    <!-- 侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">📄</span>
        <span class="logo-text">OCR识别系统</span>
      </div>
      <nav class="sidebar-nav">
        <router-link class="nav-item" to="/user/dashboard">
          <span class="nav-icon">🏠</span> 工作台
        </router-link>
        <router-link class="nav-item" to="/user/upload">
          <span class="nav-icon">📤</span> 图片识别
        </router-link>
        <router-link class="nav-item" to="/user/history">
          <span class="nav-icon">📋</span> 识别历史
        </router-link>
        <router-link class="nav-item" to="/user/profile">
          <span class="nav-icon">👤</span> 个人信息
        </router-link>
        <router-link class="nav-item" to="/user/help">
          <span class="nav-icon">❓</span> 帮助中心
        </router-link>
      </nav>
      <!-- 若是管理员，显示进入后台入口 -->
      <div v-if="store.isAdmin()" class="admin-entry" @click="router.push('/admin/stat')">
        ⚙️ 进入管理后台
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="main-wrap">
      <!-- 顶部导航 -->
      <header class="top-bar">
        <div class="top-left">
          <span class="page-breadcrumb">{{ routeTitle }}</span>
        </div>
        <div class="top-right">
          <span class="user-avatar">{{ avatarChar }}</span>
          <span class="user-name">{{ store.user?.nickname || store.user?.username }}</span>
          <button class="btn btn-outline btn-sm" @click="doLogout">退出登录</button>
        </div>
      </header>
      <main class="main-content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { store } from '../store'
import http from '../http'

const router = useRouter()
const route  = useRoute()
const toast  = inject('toast')

const titleMap = {
  '/user/dashboard': '工作台',
  '/user/upload':    '图片识别',
  '/user/history':   '识别历史',
  '/user/profile':   '个人信息',
  '/user/help':      '帮助中心'
}
const routeTitle = computed(() => titleMap[route.path] || '')
const avatarChar = computed(() => {
  const n = store.user?.nickname || store.user?.username || '?'
  return n.charAt(0).toUpperCase()
})

async function doLogout() {
  await http.post('/user/logout')
  store.setUser(null)
  toast('已退出登录')
  router.push('/login')
}
</script>

<style scoped>
.layout { display: flex; min-height: 100vh; }

.sidebar {
  width: var(--sidebar-w); background: var(--sidebar-bg);
  display: flex; flex-direction: column; flex-shrink: 0; position: fixed;
  top: 0; left: 0; height: 100vh; z-index: 100;
}
.sidebar-logo {
  display: flex; align-items: center; gap: 10px;
  padding: 20px 18px; border-bottom: 1px solid rgba(255,255,255,.08);
}
.logo-icon { font-size: 24px; }
.logo-text { font-size: 14px; font-weight: 700; color: #fff; letter-spacing: 1px; }

.sidebar-nav { flex: 1; padding: 16px 0; overflow-y: auto; }
.nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 11px 20px; color: var(--sidebar-text);
  text-decoration: none; font-size: 13px; transition: all .2s;
}
.nav-item:hover { background: rgba(255,255,255,.08); color: #fff; }
.nav-item.router-link-active { background: var(--sidebar-active); color: #fff; }
.nav-icon { font-size: 16px; width: 20px; text-align: center; }

.admin-entry {
  margin: 0 14px 20px; padding: 10px 14px; background: rgba(255,255,255,.08);
  border-radius: 8px; color: #94a3b8; font-size: 12px; cursor: pointer; text-align: center;
  transition: .2s;
}
.admin-entry:hover { background: rgba(255,255,255,.14); color: #fff; }

.main-wrap { margin-left: var(--sidebar-w); flex: 1; display: flex; flex-direction: column; min-height: 100vh; }

.top-bar {
  height: var(--header-h); background: #fff; border-bottom: 1px solid var(--border);
  display: flex; align-items: center; justify-content: space-between;
  padding: 0 24px; position: sticky; top: 0; z-index: 50;
}
.page-breadcrumb { font-size: 15px; font-weight: 600; color: var(--text-main); }
.top-right { display: flex; align-items: center; gap: 12px; }
.user-avatar {
  width: 32px; height: 32px; background: var(--primary); color: #fff;
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 700;
}
.user-name { font-size: 13px; font-weight: 500; color: var(--text-main); }

.main-content { flex: 1; padding: 24px; overflow-y: auto; }
</style>

