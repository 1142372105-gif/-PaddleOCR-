<template>
  <div>
    <div class="page-title">👤 个人信息</div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:800px">
      <!-- 基本信息 -->
      <div class="card">
        <div class="section-title">基本信息</div>
        <div class="info-row"><span class="info-label">用户名</span><span class="info-val">{{ store.user?.username }}</span></div>
        <div class="info-row"><span class="info-label">角色</span>
          <span :class="store.isAdmin()?'badge badge-blue':'badge badge-green'">
            {{ store.isAdmin() ? '管理员' : '普通用户' }}
          </span>
        </div>
        <hr style="margin:16px 0;border:none;border-top:1px solid var(--border)" />

        <!-- 修改信息表单 -->
        <div class="form-group">
          <label>昵称</label>
          <input class="form-input" v-model="form.nickname" :placeholder="store.user?.nickname||'请填写昵称'" />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input class="form-input" v-model="form.email" :placeholder="store.user?.email||'请填写邮箱'" />
        </div>
        <div class="form-group">
          <label>新密码 <small>（不填则不修改）</small></label>
          <input class="form-input" type="password" v-model="form.passwd" placeholder="不少于6位" />
        </div>
        <button class="btn btn-primary" @click="saveInfo">保存修改</button>
      </div>

      <!-- 账号安全 -->
      <div class="card">
        <div class="section-title">账号安全</div>
        <div class="security-item">
          <div class="sec-icon">🔐</div>
          <div class="sec-info">
            <div class="sec-name">安全问题</div>
            <div class="sec-desc">{{ store.user?.question || '暂未设置' }}</div>
          </div>
          <span class="badge badge-green">已设置</span>
        </div>
        <div class="security-item">
          <div class="sec-icon">📧</div>
          <div class="sec-info">
            <div class="sec-name">绑定邮箱</div>
            <div class="sec-desc">{{ store.user?.email || '暂未绑定' }}</div>
          </div>
          <span :class="store.user?.email ? 'badge badge-green' : 'badge badge-gray'">
            {{ store.user?.email ? '已绑定' : '未绑定' }}
          </span>
        </div>
        <div class="security-item">
          <div class="sec-icon">📅</div>
          <div class="sec-info">
            <div class="sec-name">注册时间</div>
            <div class="sec-desc">{{ userCreatedat }}</div>
          </div>
        </div>

        <div style="margin-top:20px">
          <div class="section-title">温馨提示</div>
          <ul class="tips-list">
            <li>请定期修改账号密码保证安全</li>
            <li>安全问题用于找回密码，请牢记答案</li>
            <li>如有问题请联系系统管理员</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, computed, inject, onMounted, ref } from 'vue'
import { store } from '../../store'
import http from '../../http'

const toast = inject('toast')
const form = reactive({ nickname: '', email: '', passwd: '' })
const userCreatedat = ref('')

onMounted(async () => {
  // 获取完整用户信息
  const res = await http.get('/user/info', { params: { uid: store.user?.id } })
  if (res.code === 200) {
    userCreatedat.value = res.data.createdat
  }
})

async function saveInfo() {
  const payload = { uid: store.user?.id }
  if (form.nickname) payload.nickname = form.nickname
  if (form.email) payload.email = form.email
  if (form.passwd) payload.passwd = form.passwd

  if (Object.keys(payload).length <= 1) {
    toast('请填写要修改的内容', 'warning')
    return
  }

  const res = await http.post('/user/update_info', payload)
  if (res.code === 200) {
    // 更新本地store
    if (form.nickname) store.user.nickname = form.nickname
    if (form.email) store.user.email = form.email
    store.setUser(store.user)
    toast('个人信息已更新')
    form.nickname = ''; form.email = ''; form.passwd = ''
  } else {
    toast(res.msg, 'error')
  }
}
</script>

<style scoped>
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 14px; color: var(--text-main); }
.info-row { display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }
.info-label { width: 60px; color: var(--text-sub); font-size: 13px; }
.info-val { font-size: 13px; font-weight: 500; }
small { color: var(--text-sub); font-size: 11px; }
.security-item { display: flex; align-items: center; gap: 12px; padding: 12px 0; border-bottom: 1px solid var(--border); }
.sec-icon { font-size: 22px; width: 36px; text-align: center; }
.sec-info { flex: 1; }
.sec-name { font-size: 13px; font-weight: 500; }
.sec-desc { font-size: 12px; color: var(--text-sub); margin-top: 2px; }
.tips-list { padding-left: 16px; color: var(--text-sub); font-size: 12px; line-height: 2; }
</style>

