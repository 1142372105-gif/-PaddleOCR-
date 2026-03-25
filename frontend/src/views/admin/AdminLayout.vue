<template>
  <div class="layout">
    <!-- 管理员侧边栏 -->
    <aside class="sidebar">
      <div class="sidebar-logo">
        <span class="logo-icon">⚙️</span>
        <span class="logo-text">OCR管理后台</span>
      </div>
      <nav class="sidebar-nav">
        <router-link class="nav-item" to="/admin/stat">
          <span class="nav-icon">📊</span> 统计分析
        </router-link>
        <router-link class="nav-item" to="/admin/users">
          <span class="nav-icon">👥</span> 用户管理
        </router-link>
        <router-link class="nav-item" to="/admin/config">
          <span class="nav-icon">🔧</span> 系统配置
        </router-link>
        <router-link class="nav-item" to="/admin/log">
          <span class="nav-icon">📝</span> 操作日志
        </router-link>
      </nav>
      <div class="back-user" @click="router.push('/user/dashboard')">
        ← 返回用户中心
      </div>
    </aside>

    <!-- 主内容区 -->
    <div class="main-wrap">
      <header class="top-bar">
        <div class="top-left">
          <span class="page-breadcrumb">{{ routeTitle }}</span>
        </div>
        <div class="top-right">
          <span class="admin-badge">管理员</span>
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
import { store } from '../../store'
import http from '../../http'

const router = useRouter()
const route  = useRoute()
const toast  = inject('toast')

const titleMap = {
  '/admin/stat':   '统计分析',
  '/admin/users':  '用户管理',
  '/admin/config': '系统配置',
  '/admin/log':    '操作日志'
}
const routeTitle = computed(() => titleMap[route.path] || '管理后台')

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
  width: var(--sidebar-w); background: #0c1527;
  display: flex; flex-direction: column; flex-shrink: 0;
  position: fixed; top: 0; left: 0; height: 100vh; z-index: 100;
}
.sidebar-logo { display: flex; align-items: center; gap: 10px; padding: 20px 18px; border-bottom: 1px solid rgba(255,255,255,.08); }
.logo-icon { font-size: 22px; }
.logo-text { font-size: 13px; font-weight: 700; color: #fff; }
.sidebar-nav { flex: 1; padding: 16px 0; overflow-y: auto; }
.nav-item { display: flex; align-items: center; gap: 10px; padding: 11px 20px; color: #94a3b8; text-decoration: none; font-size: 13px; transition: .2s; }
.nav-item:hover { background: rgba(255,255,255,.08); color: #fff; }
.nav-item.router-link-active { background: var(--primary); color: #fff; }
.nav-icon { font-size: 16px; width: 20px; text-align: center; }
.back-user { margin: 0 14px 20px; padding: 10px 14px; background: rgba(255,255,255,.06); border-radius: 8px; color: #64748b; font-size: 12px; cursor: pointer; text-align: center; transition: .2s; }
.back-user:hover { background: rgba(255,255,255,.12); color: #fff; }
.main-wrap { margin-left: var(--sidebar-w); flex: 1; display: flex; flex-direction: column; }
.top-bar { height: var(--header-h); background: #fff; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; padding: 0 24px; position: sticky; top: 0; z-index: 50; }
.page-breadcrumb { font-size: 15px; font-weight: 600; }
.top-right { display: flex; align-items: center; gap: 12px; }
.admin-badge { background: #fef9c3; color: #a16207; padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700; }
.user-name { font-size: 13px; font-weight: 500; }
.main-content { flex: 1; padding: 24px; overflow-y: auto; background: var(--bg); }
</style>

