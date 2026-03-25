<template>
  <div>
    <div class="page-title">📋 识别历史</div>

    <!-- 搜索区 -->
    <div class="card" style="margin-bottom:16px">
      <div class="search-bar">
        <select class="form-select" style="width:120px" v-model="filterLang" @change="load(1)">
          <option value="">全部语言</option>
          <option v-for="l in langs" :key="l.code" :value="l.code">{{ l.name }}</option>
        </select>
        <select class="form-select" style="width:120px" v-model="filterStatus" @change="load(1)">
          <option value="">全部状态</option>
          <option value="1">成功</option>
          <option value="2">失败</option>
          <option value="0">处理中</option>
        </select>
        <button class="btn btn-outline" @click="load(1)">🔄 刷新</button>
      </div>

      <table class="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>文件名</th>
            <th>语言</th>
            <th>识别结果预览</th>
            <th>置信度</th>
            <th>状态</th>
            <th>时间</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="list.length===0">
            <td colspan="8" class="tip-empty">暂无识别记录</td>
          </tr>
          <tr v-for="r in list" :key="r.id">
            <td>{{ r.id }}</td>
            <td>{{ r.imgname }}</td>
            <td><span class="badge badge-blue">{{ r.lang }}</span></td>
            <td class="result-preview">{{ (r.result||'').slice(0,40) }}{{ (r.result||'').length>40?'...':'' }}</td>
            <td>
              <div class="conf-bar">
                <div class="conf-track"><div class="conf-fill" :style="{width:(r.confidence*100)+'%'}"></div></div>
                <span>{{ (r.confidence*100).toFixed(1) }}%</span>
              </div>
            </td>
            <td><span :class="statusBadge(r.status)">{{ statusText(r.status) }}</span></td>
            <td>{{ r.createdat }}</td>
            <td>
              <div class="action-btns">
                <button class="btn btn-outline btn-sm" @click="openDetail(r)">详情</button>
                <button class="btn btn-danger btn-sm" @click="delRecord(r.id)">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- 分页 -->
      <div class="pagination">
        <button :disabled="page<=1" @click="load(page-1)">上一页</button>
        <button v-for="p in totalPages" :key="p" :class="{active:p===page}" @click="load(p)">{{ p }}</button>
        <button :disabled="page>=totalPages" @click="load(page+1)">下一页</button>
        <span style="font-size:12px;color:var(--text-sub)">共{{ total }}条</span>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <div class="modal-mask" v-if="detailVisible" @click.self="detailVisible=false">
      <div class="modal-box" style="width:600px">
        <div class="modal-title">📄 识别结果详情</div>
        <div class="detail-info">
          <div class="di-row"><span class="di-label">文件名：</span>{{ detailRow.imgname }}</div>
          <div class="di-row"><span class="di-label">识别语言：</span>{{ detailRow.lang }}</div>
          <div class="di-row">
            <span class="di-label">置信度：</span>{{ (detailRow.confidence*100).toFixed(2) }}%
          </div>
          <div class="di-row"><span class="di-label">状态：</span>{{ statusText(detailRow.status) }}</div>
          <div class="di-row"><span class="di-label">时间：</span>{{ detailRow.createdat }}</div>
        </div>
        <div class="form-group" style="margin-top:12px">
          <label>识别文本（可编辑修正）</label>
          <textarea class="form-textarea" style="height:200px" v-model="detailRow.result" />
        </div>
        <div class="modal-footer">
          <button class="btn btn-success" @click="saveDetail">保存修改</button>
          <button class="btn btn-outline" @click="downloadText(detailRow.result, detailRow.imgname)">导出TXT</button>
          <button class="btn btn-outline" @click="detailVisible=false">关闭</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, inject } from 'vue'
import { store } from '../../store'
import http from '../../http'

const toast = inject('toast')
const list = ref([])
const langs = ref([])
const page = ref(1)
const total = ref(0)
const size = 10
const filterLang = ref('')
const filterStatus = ref('')
const totalPages = computed(() => Math.max(1, Math.ceil(total.value / size)))

const detailVisible = ref(false)
const detailRow = ref({})

function statusText(s) { return s===1?'成功':s===2?'失败':'处理中' }
function statusBadge(s) { return s===1?'badge badge-green':s===2?'badge badge-red':'badge badge-yellow' }

async function load(p = 1) {
  page.value = p
  const uid = store.user?.id
  const res = await http.get('/record/list', { params: { uid, page: p, size } })
  if (res.code === 200) {
    // 前端过滤语言和状态
    let data = res.data.list
    if (filterLang.value) data = data.filter(r => r.lang === filterLang.value)
    if (filterStatus.value !== '') data = data.filter(r => r.status === Number(filterStatus.value))
    list.value = data
    total.value = res.data.total
  }
}

onMounted(async () => {
  load(1)
  const res = await http.get('/record/langs')
  if (res.code === 200) langs.value = res.data
})

function openDetail(r) { detailRow.value = { ...r }; detailVisible.value = true }

async function saveDetail() {
  const res = await http.post('/record/update', { id: detailRow.value.id, result: detailRow.value.result })
  if (res.code === 200) { toast('已保存'); detailVisible.value = false; load(page.value) }
  else toast(res.msg, 'error')
}

async function delRecord(id) {
  if (!confirm('确认删除该识别记录？')) return
  const res = await http.post('/record/delete', { id })
  if (res.code === 200) { toast('已删除'); load(page.value) }
  else toast(res.msg, 'error')
}

function downloadText(text, fname) {
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob([text||''], { type: 'text/plain;charset=utf-8' }))
  a.download = (fname||'ocr').replace(/\.[^.]+$/, '') + '_ocr.txt'
  a.click()
}
</script>

<style scoped>
.result-preview { max-width: 180px; color: var(--text-sub); font-size: 12px; }
.action-btns { display: flex; gap: 5px; }
.di-row { display: flex; margin-bottom: 8px; font-size: 13px; }
.di-label { width: 90px; color: var(--text-sub); flex-shrink: 0; }
</style>

