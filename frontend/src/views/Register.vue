<template>
  <div class="auth-page">
    <div class="auth-box">
      <div class="auth-logo">📄</div>
      <h2 class="auth-title">注册新账号</h2>

      <div class="form-group">
        <label>用户名 <span class="req">*</span></label>
        <input class="form-input" v-model="form.username" placeholder="3~50位字母数字" />
      </div>
      <div class="form-group">
        <label>密码 <span class="req">*</span></label>
        <input class="form-input" type="password" v-model="form.passwd" placeholder="不少于6位" />
      </div>
      <div class="form-group">
        <label>昵称</label>
        <input class="form-input" v-model="form.nickname" placeholder="可选，展示名称" />
      </div>
      <div class="form-group">
        <label>邮箱</label>
        <input class="form-input" v-model="form.email" placeholder="可选" />
      </div>
      <div class="form-group">
        <label>安全问题 <span class="req">*</span><small>（用于找回密码）</small></label>
        <select class="form-select" v-model="form.question">
          <option value="">请选择安全问题</option>
          <option>您的出生城市是哪里？</option>
          <option>您母亲的姓名是什么？</option>
          <option>您的小学名称是什么？</option>
          <option>您的第一辆车品牌？</option>
          <option>您最喜欢的颜色？</option>
          <option>您宠物的名字？</option>
          <option>您的毕业大学名称？</option>
        </select>
      </div>
      <div class="form-group">
        <label>安全答案 <span class="req">*</span></label>
        <input class="form-input" v-model="form.answer" placeholder="请输入安全问题答案" />
      </div>

      <button class="btn btn-primary reg-btn" :disabled="loading" @click="doRegister">
        {{ loading ? '注册中...' : '立即注册' }}
      </button>
      <div class="go-login">
        已有账号？<router-link to="/login">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import http from '../http'

const router = useRouter()
const toast = inject('toast')
const loading = ref(false)

const form = reactive({ username: '', passwd: '', nickname: '', email: '', question: '', answer: '' })

async function doRegister() {
  if (!form.username || !form.passwd) { toast('用户名和密码为必填项', 'warning'); return }
  if (!form.question || !form.answer) { toast('请设置安全问题和答案，用于找回密码', 'warning'); return }
  loading.value = true
  try {
    const res = await http.post('/user/register', form)
    if (res.code === 200) {
      toast('注册成功！请登录')
      router.push('/login')
    } else {
      toast(res.msg, 'error')
    }
  } catch {
    toast('网络错误', 'error')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh; display: flex; align-items: center;
  justify-content: center; background: var(--bg);
}
.auth-box {
  width: 440px; background: #fff; border-radius: 16px;
  padding: 36px 40px; box-shadow: 0 4px 20px rgba(0,0,0,.08);
}
.auth-logo { font-size: 40px; text-align: center; margin-bottom: 8px; }
.auth-title { font-size: 20px; font-weight: 700; text-align: center; margin-bottom: 24px; }
.req { color: var(--danger); }
small { color: var(--text-sub); font-size: 11px; margin-left: 4px; }
.reg-btn { width: 100%; justify-content: center; padding: 11px; margin-top: 4px; }
.go-login { text-align: center; margin-top: 14px; font-size: 13px; color: var(--text-sub); }
.go-login a { color: var(--primary); text-decoration: none; }
</style>

