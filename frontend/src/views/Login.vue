<template>
  <div class="login-page">
    <!-- 左侧品牌区 -->
    <div class="brand-panel">
      <div class="brand-logo">📄</div>
      <h1 class="brand-title">PaddleOCR</h1>
      <p class="brand-sub">智能文本识别系统</p>
      <div class="brand-features">
        <div class="feat-item"><span class="feat-icon">🔍</span>精准文本检测</div>
        <div class="feat-item"><span class="feat-icon">🌐</span>多语言识别支持</div>
        <div class="feat-item"><span class="feat-icon">⚡</span>PP-OCRv3极速引擎</div>
        <div class="feat-item"><span class="feat-icon">📊</span>识别结果管理</div>
      </div>
    </div>

    <!-- 右侧登录表单 -->
    <div class="form-panel">
      <div class="login-box">
        <h2 class="login-title">欢迎登录</h2>
        <p class="login-desc">请输入您的账号和密码</p>

        <div class="form-group">
          <label>用户名</label>
          <input class="form-input" v-model="form.username" placeholder="请输入用户名" @keyup.enter="doLogin" />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input class="form-input" type="password" v-model="form.passwd" placeholder="请输入密码" @keyup.enter="doLogin" />
        </div>

        <button class="btn btn-primary login-btn" :disabled="loading" @click="doLogin">
          {{ loading ? '登录中...' : '立即登录' }}
        </button>

        <div class="login-links">
          <router-link to="/register">注册新账号</router-link>
          <router-link to="/findpwd">忘记密码？</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import http from '../http'
import { store } from '../store'

const router = useRouter()
const toast = inject('toast')
const loading = ref(false)

const form = reactive({ username: '', passwd: '' })

async function doLogin() {
  if (!form.username || !form.passwd) { toast('请填写用户名和密码', 'warning'); return }
  loading.value = true
  try {
    const res = await http.post('/user/login', form)
    if (res.code === 200) {
      store.setUser(res.data)
      toast('登录成功，欢迎回来！')
      // 管理员跳管理后台，普通用户跳用户中心
      router.push(res.data.role === 1 ? '/admin/stat' : '/user/dashboard')
    } else {
      toast(res.msg, 'error')
    }
  } catch {
    toast('网络请求失败', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh; display: flex;
}
.brand-panel {
  width: 420px; background: var(--sidebar-bg); color: #fff;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 60px 40px; flex-shrink: 0;
}
.brand-logo { font-size: 72px; margin-bottom: 16px; }
.brand-title { font-size: 32px; font-weight: 700; letter-spacing: 2px; }
.brand-sub { font-size: 14px; color: #94a3b8; margin-top: 8px; margin-bottom: 48px; }
.brand-features { width: 100%; display: flex; flex-direction: column; gap: 16px; }
.feat-item {
  display: flex; align-items: center; gap: 12px;
  padding: 14px 18px; background: rgba(255,255,255,.07);
  border-radius: 10px; font-size: 14px; color: #cbd5e1;
}
.feat-icon { font-size: 20px; }

.form-panel {
  flex: 1; display: flex; align-items: center; justify-content: center;
  background: var(--bg);
}
.login-box { width: 400px; background: #fff; border-radius: 16px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,.08); }
.login-title { font-size: 24px; font-weight: 700; margin-bottom: 6px; }
.login-desc { color: var(--text-sub); font-size: 13px; margin-bottom: 28px; }
.login-btn { width: 100%; justify-content: center; padding: 11px; font-size: 15px; margin-top: 8px; }
.login-links { display: flex; justify-content: space-between; margin-top: 16px; }
.login-links a { color: var(--primary); font-size: 13px; text-decoration: none; }
.login-links a:hover { text-decoration: underline; }

@media (max-width: 700px) {
  .brand-panel { display: none; }
  .login-box { width: 90%; }
}
</style>

