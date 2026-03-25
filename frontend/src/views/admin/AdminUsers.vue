<template>
  <div>
    <div class="page-title">👥 用户管理</div>

    <!-- 搜索+新增 -->
    <div class="card" style="margin-bottom:16px">
      <div class="search-bar">
        <input class="form-input" style="width:220px" v-model="keyword" placeholder="搜索用户名/昵称" @keyup.enter="load(1)" />
        <button class="btn btn-primary" @click="load(1)">🔍 搜索</button>
        <button class="btn btn-success" @click="openAdd">+ 新增用户</button>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th><th>用户名</th><th>昵称</th><th>邮箱</th>
            <th>角色</th><th>状态</th><th>注册时间</th><th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="list.length===0"><td colspan="8" class="tip-empty">暂无数据</td></tr>
          <tr v-for="u in list" :key="u.id">
            <td>{{ u.id }}</td>
            <td>{{ u.username }}</td>
            <td>{{ u.nickname }}</td>
            <td>{{ u.email }}</td>
            <td>
              <span :class="u.role===1?'badge badge-yellow':'badge badge-blue'">
                {{ u.role===1?'管理员':'普通用户' }}
              </span>
            </td>
            <td>
              <span :class="u.status===1?'badge badge-green':'badge badge-red'">
                {{ u.status===1?'启用':'禁用' }}
              </span>
            </td>
            <td>{{ u.createdat }}</td>
            <td>
              <div class="action-btns">
                <button class="btn btn-outline btn-sm" @click="openEdit(u)">编辑</button>
                <button class="btn btn-warning btn-sm" @click="toggleStatus(u)">
                  {{ u.status===1?'禁用':'启用' }}
                </button>
                <button class="btn btn-danger btn-sm" @click="delUser(u.id)">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <div class="pagination">
        <button :disabled="page<=1" @click="load(page-1)">上一页</button>
        <button v-for="p in totalPages" :key="p" :class="{active:p===page}" @click="load(p)">{{ p }}</button>
        <button :disabled="page>=totalPages" @click="load(page+1)">下一页</button>
        <span style="font-size:12px;color:var(--text-sub)">共{{ total }}条</span>
      </div>
    </div>

    <!-- 新增/编辑弹窗 -->
    <div class="modal-mask" v-if="modalVisible" @click.self="modalVisible=false">
      <div class="modal-box">
        <div class="modal-title">{{ editMode?'编辑用户':'新增用户' }}</div>
        <div class="form-group">
          <label>用户名</label>
          <input class="form-input" v-model="form.username" :disabled="editMode" />
        </div>
        <div class="form-group">
          <label>密码{{ editMode?' (不填则不修改)':'' }}</label>
          <input class="form-input" type="password" v-model="form.passwd" placeholder="默认123456" />
        </div>
        <div class="form-group">
          <label>昵称</label>
          <input class="form-input" v-model="form.nickname" />
        </div>
        <div class="form-group">
          <label>邮箱</label>
          <input class="form-input" v-model="form.email" />
        </div>
        <div class="form-group">
          <label>角色</label>
          <select class="form-select" v-model="form.role">
            <option :value="0">普通用户</option>
            <option :value="1">管理员</option>
          </select>
        </div>
        <div class="modal-footer">
          <button class="btn btn-primary" @click="saveUser">保存</button>
          <button class="btn btn-outline" @click="modalVisible=false">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, inject } from 'vue'
import http from '../../http'

const toast = inject('toast')
const list = ref([])
const keyword = ref('')
const page = ref(1)
const total = ref(0)
const size = 10
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / size)))
const modalVisible = ref(false)
const editMode = ref(false)
const form = reactive({ id: null, username: '', passwd: '', nickname: '', email: '', role: 0 })

async function load(p = 1) {
  page.value = p
  const res = await http.get('/admin/user/list', { params: { keyword: keyword.value, page: p, size } })
  if (res.code === 200) { list.value = res.data.list; total.value = res.data.total }
}
onMounted(() => load(1))

function openAdd() {
  editMode.value = false
  Object.assign(form, { id: null, username: '', passwd: '', nickname: '', email: '', role: 0 })
  modalVisible.value = true
}
function openEdit(u) {
  editMode.value = true
  Object.assign(form, { id: u.id, username: u.username, passwd: '', nickname: u.nickname, email: u.email, role: u.role })
  modalVisible.value = true
}

async function saveUser() {
  if (!editMode.value) {
    if (!form.username) { toast('请填写用户名', 'warning'); return }
    const res = await http.post('/admin/user/add', { ...form, passwd: form.passwd || '123456' })
    if (res.code === 200) { toast('用户已添加'); modalVisible.value = false; load(1) }
    else toast(res.msg, 'error')
  } else {
    const payload = { id: form.id, nickname: form.nickname, email: form.email, role: form.role }
    if (form.passwd) payload.passwd = form.passwd
    const res = await http.post('/admin/user/update', payload)
    if (res.code === 200) { toast('用户已更新'); modalVisible.value = false; load(page.value) }
    else toast(res.msg, 'error')
  }
}

async function toggleStatus(u) {
  const ns = u.status === 1 ? 0 : 1
  const res = await http.post('/admin/user/update', { id: u.id, status: ns })
  if (res.code === 200) { toast(`已${ns===1?'启用':'禁用'}用户`); load(page.value) }
}

async function delUser(id) {
  if (!confirm('确认删除该用户？其所有识别记录也将删除')) return
  const res = await http.post('/admin/user/delete', { id })
  if (res.code === 200) { toast('用户已删除'); load(page.value) }
}
</script>

<style scoped>
.action-btns { display: flex; gap: 5px; flex-wrap: wrap; }
</style>

