<template>
  <div class="auth-page">
    <div class="auth-box">
      <div class="auth-logo">🔐</div>
      <h2 class="auth-title">找回密码</h2>

      <!-- 第一步：输入用户名查安全问题 -->
      <template v-if="step === 1">
        <div class="form-group">
          <label>用户名</label>
          <input class="form-input" v-model="username" placeholder="请输入注册时的用户名" />
        </div>
        <button class="btn btn-primary w-full" @click="fetchQuestion">下一步</button>
      </template>

      <!-- 第二步：回答安全问题并设置新密码 -->
      <template v-if="step === 2">
        <div class="question-box">
          <span class="q-label">安全问题：</span>
          <span class="q-text">{{ question }}</span>
        </div>
        <div class="form-group">
          <label>安全答案</label>
          <input class="form-input" v-model="answer" placeholder="请回答安全问题" />
        </div>
        <div class="form-group">
          <label>新密码</label>
          <input class="form-input" type="password" v-model="newpasswd" placeholder="不少于6位" />
        </div>
        <button class="btn btn-primary w-full" :disabled="loading" @click="doReset">
          {{ loading ? '重置中...' : '重置密码' }}
        </button>
      </template>

      <div class="go-login">
        <router-link to="/login">← 返回登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, inject } from 'vue'
import { useRouter } from 'vue-router'
import http from '../http'

const router = useRouter()
const toast = inject('toast')

const step = ref(1)
const username = ref('')
const question = ref('')
const answer = ref('')
const newpasswd = ref('')
const loading = ref(false)

async function fetchQuestion() {
  if (!username.value.trim()) { toast('请输入用户名', 'warning'); return }
  const res = await http.get('/user/get_question', { params: { username: username.value } })
  if (res.code === 200) {
    question.value = res.data.question
    step.value = 2
  } else {
    toast(res.msg, 'error')
  }
}

async function doReset() {
  if (!answer.value || !newpasswd.value) { toast('请填写完整', 'warning'); return }
  loading.value = true
  try {
    const res = await http.post('/user/find_password', {
      username: username.value, answer: answer.value, newpasswd: newpasswd.value
    })
    if (res.code === 200) {
      toast('密码已重置，请用新密码登录')
      router.push('/login')
    } else {
      toast(res.msg, 'error')
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; background: var(--bg); }
.auth-box { width: 420px; background: #fff; border-radius: 16px; padding: 36px 40px; box-shadow: 0 4px 20px rgba(0,0,0,.08); }
.auth-logo { font-size: 40px; text-align: center; margin-bottom: 8px; }
.auth-title { font-size: 20px; font-weight: 700; text-align: center; margin-bottom: 24px; }
.w-full { width: 100%; justify-content: center; padding: 11px; }
.question-box { background: #f1f5f9; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px; }
.q-label { font-weight: 600; color: var(--text-sub); font-size: 12px; display: block; margin-bottom: 4px; }
.q-text { color: var(--text-main); font-size: 14px; }
.go-login { text-align: center; margin-top: 16px; }
.go-login a { color: var(--primary); font-size: 13px; text-decoration: none; }
</style>

