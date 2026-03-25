// 路由配置
import { createRouter, createWebHistory } from 'vue-router'
import { store } from './store'

// 页面组件懒加载
const Login       = () => import('./views/Login.vue')
const Register    = () => import('./views/Register.vue')
const FindPwd     = () => import('./views/FindPwd.vue')
const Layout      = () => import('./views/Layout.vue')
const Dashboard   = () => import('./views/user/Dashboard.vue')
const UploadOCR   = () => import('./views/user/UploadOCR.vue')
const History     = () => import('./views/user/History.vue')
const Profile     = () => import('./views/user/Profile.vue')
const Help        = () => import('./views/user/Help.vue')
const AdminLayout = () => import('./views/admin/AdminLayout.vue')
const AdminUsers  = () => import('./views/admin/AdminUsers.vue')
const AdminConfig = () => import('./views/admin/AdminConfig.vue')
const AdminLog    = () => import('./views/admin/AdminLog.vue')
const AdminStat   = () => import('./views/admin/AdminStat.vue')

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login',    component: Login },
  { path: '/register', component: Register },
  { path: '/findpwd',  component: FindPwd },

  // 普通用户区域
  {
    path: '/user',
    component: Layout,
    meta: { requireLogin: true },
    children: [
      { path: '',          redirect: 'dashboard' },
      { path: 'dashboard', component: Dashboard },
      { path: 'upload',    component: UploadOCR },
      { path: 'history',   component: History },
      { path: 'profile',   component: Profile },
      { path: 'help',      component: Help }
    ]
  },

  // 管理员区域
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requireLogin: true, requireAdmin: true },
    children: [
      { path: '',       redirect: 'stat' },
      { path: 'stat',   component: AdminStat },
      { path: 'users',  component: AdminUsers },
      { path: 'config', component: AdminConfig },
      { path: 'log',    component: AdminLog }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  if (to.meta.requireLogin && !store.isLogin()) {
    next('/login')
    return
  }
  if (to.meta.requireAdmin && !store.isAdmin()) {
    next('/user/dashboard')
    return
  }
  next()
})

export default router

