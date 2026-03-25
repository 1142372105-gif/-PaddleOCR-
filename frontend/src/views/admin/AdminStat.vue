<template>
  <div>
    <div class="page-title">📊 统计分析</div>

    <!-- 总览卡片 -->
    <div class="stat-grid">
      <div class="stat-card">
        <div class="stat-icon blue">👥</div>
        <div><div class="stat-num">{{ overview.totalUser }}</div><div class="stat-label">注册用户数</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon green">📋</div>
        <div><div class="stat-num">{{ overview.totalRecord }}</div><div class="stat-label">总识别次数</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon yellow">✅</div>
        <div><div class="stat-num">{{ overview.successRecord }}</div><div class="stat-label">识别成功次数</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon purple">📈</div>
        <div><div class="stat-num">{{ (overview.avgConfidence*100).toFixed(1) }}%</div><div class="stat-label">平均置信度</div></div>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">
      <!-- 按月识别趋势 -->
      <div class="card">
        <div class="section-title">📅 月度识别趋势</div>
        <div v-if="monthly.length===0" class="tip-empty">暂无数据</div>
        <div v-else class="chart-wrap">
          <div class="chart-bar-group" v-for="m in monthly" :key="m.mon">
            <div class="chart-bar-wrap">
              <div class="chart-bar success-bar" :style="{height: barH(m.success,maxCnt)+'px'}" :title="`成功:${m.success}`"></div>
              <div class="chart-bar fail-bar" :style="{height: barH(m.fail,maxCnt)+'px'}" :title="`失败:${m.fail}`"></div>
            </div>
            <div class="chart-label">{{ m.mon.slice(5) }}</div>
            <div class="chart-cnt">{{ m.cnt }}</div>
          </div>
        </div>
        <div class="chart-legend">
          <span><span class="leg success-bar"></span>成功</span>
          <span><span class="leg fail-bar"></span>失败</span>
        </div>
      </div>

      <!-- 各语言识别准确率 -->
      <div class="card">
        <div class="section-title">🌐 各语言识别情况</div>
        <div v-if="accuracy.length===0" class="tip-empty">暂无数据</div>
        <table v-else class="data-table">
          <thead>
            <tr>
              <th>语言</th>
              <th>总次数</th>
              <th>成功</th>
              <th>平均置信度</th>
              <th>成功率</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in accuracy" :key="a.lang">
              <td><span class="badge badge-blue">{{ a.lang }}</span></td>
              <td>{{ a.total }}</td>
              <td>{{ a.success }}</td>
              <td>{{ (a.avgconf*100).toFixed(1) }}%</td>
              <td>
                <div class="conf-bar">
                  <div class="conf-track">
                    <div class="conf-fill" :style="{width:(a.total>0?a.success/a.total*100:0)+'%'}"></div>
                  </div>
                  <span>{{ a.total>0?((a.success/a.total)*100).toFixed(0):0 }}%</span>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import http from '../../http'

const overview = ref({ totalUser: 0, totalRecord: 0, successRecord: 0, avgConfidence: 0 })
const monthly = ref([])
const accuracy = ref([])

const maxCnt = computed(() => Math.max(1, ...monthly.value.map(m => m.cnt)))
function barH(val, max) { return Math.max(4, Math.round((val / max) * 120)) }

onMounted(async () => {
  const [r1, r2, r3] = await Promise.all([
    http.get('/admin/stat/overview'),
    http.get('/admin/stat/monthly'),
    http.get('/admin/stat/accuracy')
  ])
  if (r1.code === 200) overview.value = r1.data
  if (r2.code === 200) monthly.value = r2.data
  if (r3.code === 200) accuracy.value = r3.data
})
</script>

<style scoped>
.stat-icon.purple { background: #ede9fe; }
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 16px; color: var(--text-main); }

/* 柱状图 */
.chart-wrap { display: flex; align-items: flex-end; gap: 12px; height: 160px; padding-bottom: 28px; overflow-x: auto; }
.chart-bar-group { display: flex; flex-direction: column; align-items: center; gap: 2px; min-width: 36px; }
.chart-bar-wrap { display: flex; align-items: flex-end; gap: 2px; }
.chart-bar { width: 14px; border-radius: 3px 3px 0 0; transition: height .4s; }
.success-bar { background: var(--success); }
.fail-bar    { background: var(--danger); }
.chart-label { font-size: 11px; color: var(--text-sub); margin-top: 4px; }
.chart-cnt   { font-size: 11px; font-weight: 700; color: var(--text-main); }
.chart-legend { display: flex; gap: 16px; margin-top: 8px; font-size: 12px; color: var(--text-sub); }
.leg { display: inline-block; width: 12px; height: 12px; border-radius: 2px; margin-right: 4px; vertical-align: middle; }
</style>

