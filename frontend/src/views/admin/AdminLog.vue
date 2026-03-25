<template>
  <div>
    <div class="page-title">📝 操作日志</div>

    <div class="card">
      <!-- 搜索 + 操作按钮 -->
      <div class="search-bar">
        <input class="form-input" style="width:240px" v-model="keyword" placeholder="搜索操作动作/详情" @keyup.enter="load(1)" />
        <button class="btn btn-primary" @click="load(1)">🔍 搜索</button>
        <button class="btn btn-outline" @click="exportLog">⬇ 导出CSV</button>
        <button class="btn btn-danger" @click="clearLog">🗑 清空历史日志</button>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>操作用户</th>
            <th>操作动作</th>
            <th>操作详情</th>
            <th>IP地址</th>
            <th>操作时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="list.length===0">
            <td colspan="6" class="tip-empty">暂无日志数据</td>
          </tr>
          <tr v-for="log in list" :key="log.id">
            <td>{{ log.id }}</td>
            <td>
              <span v-if="log.username" class="badge badge-blue">{{ log.username }}</span>
              <span v-else class="badge badge-gray">系统</span>
            </td>
            <td>
              <span class="action-tag" :class="getActionClass(log.action)">{{ log.action }}</span>
            </td>
            <td class="log-detail">{{ log.detail }}</td>
            <td style="font-size:12px;color:var(--text-sub)">{{ log.ip }}</td>
            <td style="font-size:12px;white-space:nowrap">{{ log.createdat }}</td>
          </tr>
        </tbody>
      </table>

      <!-- 分页 -->
      <div class="pagination">
        <button :disabled="page<=1" @click="load(page-1)">上一页</button>
        <button v-for="p in showPages" :key="p" :class="{active:p===page}" @click="load(p)">{{ p }}</button>
        <button :disabled="page>=totalPages" @click="load(page+1)">下一页</button>
        <span style="font-size:12px;color:var(--text-sub)">共{{ total }}条 / {{ totalPages }}页</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import http from '../../http'

const toast = inject('toast')
const list = ref([])
const keyword = ref('')
const page = ref(1)
const total = ref(0)
const size = 20
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / size)))
const showPages = computed(() => {
  const pages = []
  for (let i = Math.max(1, page.value - 2); i <= Math.min(totalPages.value, page.value + 2); i++) pages.push(i)
  return pages
})

async function load(p = 1) {
  page.value = p
  const res = await http.get('/admin/log/list', { params: { keyword: keyword.value, page: p, size } })
  if (res.code === 200) { list.value = res.data.list; total.value = res.data.total }
}
onMounted(() => load(1))

function getActionClass(action) {
  if (action.includes('登录')) return 'tag-info'
  if (action.includes('删除') || action.includes('清空')) return 'tag-danger'
  if (action.includes('添加') || action.includes('注册')) return 'tag-success'
  if (action.includes('修改') || action.includes('更新') || action.includes('导出')) return 'tag-warning'
  return 'tag-default'
}

function exportLog() {
  window.open('/api/admin/log/export', '_blank')
}

async function clearLog() {
  if (!confirm('确认清空30天前的历史日志？此操作不可恢复！')) return
  const res = await http.post('/admin/log/clear')
  if (res.code === 200) { toast('历史日志已清空'); load(1) }
  else toast(res.msg, 'error')
}
</script>

<style scoped>
.log-detail { font-size: 12px; color: var(--text-sub); max-width: 240px; }
.action-tag { display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
.tag-info    { background: #dbeafe; color: #1d4ed8; }
.tag-success { background: #dcfce7; color: #15803d; }
.tag-danger  { background: #fee2e2; color: #dc2626; }
.tag-warning { background: #fef3c7; color: #d97706; }
.tag-default { background: #f1f5f9; color: #64748b; }
</style>

