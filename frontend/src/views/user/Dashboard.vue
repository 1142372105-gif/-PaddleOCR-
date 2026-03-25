<template>
  <div>
    <div class="page-title">🏠 工作台</div>

    <!-- 统计卡片 -->
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-icon blue">📊</div>
        <div>
          <div class="stat-num">{{ stat.total }}</div>
          <div class="stat-label">总识别次数</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green">✅</div>
        <div>
          <div class="stat-num">{{ stat.success }}</div>
          <div class="stat-label">成功识别</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon yellow">📈</div>
        <div>
          <div class="stat-num">{{ (stat.avgConf * 100).toFixed(1) }}%</div>
          <div class="stat-label">平均置信度</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon purple">🕐</div>
        <div>
          <div class="stat-num">{{ stat.recent }}</div>
          <div class="stat-label">近7天识别</div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="card" style="margin-bottom:20px">
      <div class="section-title">快捷操作</div>
      <div class="quick-btns">
        <button class="quick-btn" @click="router.push('/user/upload')">
          <span class="qb-icon">📤</span>
          <span>上传识别</span>
        </button>
        <button class="quick-btn" @click="router.push('/user/history')">
          <span class="qb-icon">📋</span>
          <span>查看历史</span>
        </button>
        <button class="quick-btn" @click="router.push('/user/profile')">
          <span class="qb-icon">👤</span>
          <span>个人信息</span>
        </button>
        <button class="quick-btn" @click="router.push('/user/help')">
          <span class="qb-icon">❓</span>
          <span>使用帮助</span>
        </button>
      </div>
    </div>

    <!-- 最近识别记录 -->
    <div class="card">
      <div class="section-title">最近识别记录</div>
      <div v-if="recentList.length === 0" class="tip-empty">暂无识别记录，快去上传图片吧 ~</div>
      <table v-else class="data-table">
        <thead>
          <tr>
            <th>文件名</th>
            <th>语言</th>
            <th>置信度</th>
            <th>状态</th>
            <th>时间</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in recentList" :key="r.id">
            <td>{{ r.imgname }}</td>
            <td>{{ r.lang }}</td>
            <td>
              <div class="conf-bar">
                <div class="conf-track"><div class="conf-fill" :style="{width: (r.confidence*100)+'%'}"></div></div>
                <span>{{ (r.confidence*100).toFixed(1) }}%</span>
              </div>
            </td>
            <td>
              <span :class="statusBadge(r.status)">{{ statusText(r.status) }}</span>
            </td>
            <td>{{ r.createdat }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { store } from '../../store'
import http from '../../http'

const router = useRouter()
const stat = ref({ total: 0, success: 0, avgConf: 0, recent: 0 })
const recentList = ref([])

function statusText(s) { return s === 1 ? '成功' : s === 2 ? '失败' : '处理中' }
function statusBadge(s) { return s === 1 ? 'badge badge-green' : s === 2 ? 'badge badge-red' : 'badge badge-yellow' }

onMounted(async () => {
  const uid = store.user?.id
  if (!uid) return
  const res = await http.get('/record/list', { params: { uid, page: 1, size: 5 } })
  if (res.code === 200) {
    recentList.value = res.data.list
    stat.value.total = res.data.total
    stat.value.success = res.data.list.filter(r => r.status === 1).length
    // 简单统计平均置信度
    const succ = res.data.list.filter(r => r.status === 1)
    stat.value.avgConf = succ.length
      ? succ.reduce((a, b) => a + b.confidence, 0) / succ.length : 0
    stat.value.recent = res.data.list.length
  }
})
</script>

<style scoped>
.stat-icon.purple { background: #ede9fe; }
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 14px; color: var(--text-main); }
.quick-btns { display: flex; gap: 14px; flex-wrap: wrap; }
.quick-btn {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
  padding: 20px 28px; background: var(--bg); border: 1px solid var(--border);
  border-radius: 10px; cursor: pointer; font-size: 13px; transition: all .2s;
  font-family: inherit;
}
.quick-btn:hover { border-color: var(--primary); background: var(--primary-light); color: var(--primary); }
.qb-icon { font-size: 28px; }
</style>

