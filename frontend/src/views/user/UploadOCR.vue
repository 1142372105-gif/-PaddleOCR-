<template>
  <div>
    <div class="page-title">📤 图片识别</div>

    <!-- 模式切换 -->
    <div class="card" style="margin-bottom:16px">
      <div class="mode-tabs">
        <button :class="['mode-tab', mode==='single'?'active':'']" @click="mode='single'">单张上传</button>
        <button :class="['mode-tab', mode==='batch'?'active':'']" @click="mode='batch'">批量上传</button>
      </div>
    </div>

    <!-- 上传区域 -->
    <div class="card" style="margin-bottom:16px">
      <div class="upload-options">
        <div class="form-group" style="flex:1;min-width:160px">
          <label>识别语言</label>
          <select class="form-select" v-model="lang">
            <option v-for="l in langs" :key="l.code" :value="l.code">{{ l.name }}</option>
          </select>
        </div>
      </div>

      <!-- 拖拽/点击上传区 -->
      <div
        class="upload-zone"
        :class="{ 'drag-over': dragging }"
        @click="triggerInput"
        @dragover.prevent="dragging=true"
        @dragleave="dragging=false"
        @drop.prevent="handleDrop"
      >
        <div class="upload-icon">☁️</div>
        <p style="font-size:15px;font-weight:600;color:#475569;margin-bottom:6px">
          点击选择或拖拽图片到此区域
        </p>
        <p>支持 PNG / JPG / BMP / TIFF / WEBP 格式</p>
        <p v-if="mode==='batch'" style="color:var(--primary);margin-top:4px">批量模式：可同时选择多张图片</p>
        <input ref="inputRef" type="file" style="display:none"
          :multiple="mode==='batch'" accept="image/*" @change="handleFileInput" />
      </div>

      <!-- 已选文件预览 -->
      <div v-if="selectedFiles.length" class="file-list">
        <div class="file-item" v-for="(f,i) in selectedFiles" :key="i">
          <img :src="f.preview" class="file-thumb" />
          <span class="file-fname">{{ f.file.name }}</span>
          <button class="btn btn-danger btn-sm" @click="removeFile(i)">✕</button>
        </div>
      </div>

      <button
        class="btn btn-primary" style="margin-top:16px"
        :disabled="!selectedFiles.length || loading"
        @click="doRecognize"
      >
        {{ loading ? '识别中，请稍候...' : '🔍 开始识别' }}
      </button>
    </div>

    <!-- 识别结果 -->
    <div v-if="results.length" class="card">
      <div class="page-title" style="font-size:15px;margin-bottom:14px">🎯 识别结果</div>
      <div v-for="r in results" :key="r.index" class="result-block">
        <div class="result-header">
          <span class="result-fname">{{ r.filename }}</span>
          <span :class="r.status==='ok'?'badge badge-green':'badge badge-red'">
            {{ r.status==='ok' ? '识别成功' : '识别失败' }}
          </span>
          <span v-if="r.confidence" class="badge badge-blue">
            置信度 {{ (r.confidence*100).toFixed(1) }}%
          </span>
        </div>
        <textarea class="form-textarea result-text" v-if="r.result" v-model="r.result" />
        <p v-else class="tip-empty" style="padding:16px 0">{{ r.msg || '识别失败' }}</p>
        <div v-if="r.result" style="display:flex;gap:8px;margin-top:8px">
          <button class="btn btn-success btn-sm" @click="copyText(r.result)">📋 复制</button>
          <button class="btn btn-outline btn-sm" @click="downloadText(r.result, r.filename)">⬇ 导出TXT</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import { store } from '../../store'
import http from '../../http'

const toast = inject('toast')
const mode = ref('single')
const lang = ref('ch')
const langs = ref([])
const dragging = ref(false)
const loading = ref(false)
const selectedFiles = ref([])   // [{file, preview}]
const results = ref([])
const inputRef = ref(null)

onMounted(async () => {
  const res = await http.get('/record/langs')
  if (res.code === 200) langs.value = res.data
})

function triggerInput() { inputRef.value?.click() }

function addFiles(files) {
  if (mode.value === 'single') selectedFiles.value = []
  for (const f of files) {
    if (!f.type.startsWith('image/')) continue
    const url = URL.createObjectURL(f)
    selectedFiles.value.push({ file: f, preview: url })
  }
}

function handleFileInput(e) { addFiles(Array.from(e.target.files)); e.target.value = '' }
function handleDrop(e) { dragging.value = false; addFiles(Array.from(e.dataTransfer.files)) }
function removeFile(i) { selectedFiles.value.splice(i, 1) }

async function doRecognize() {
  if (!selectedFiles.value.length) return
  loading.value = true
  results.value = []
  const uid = store.user?.id

  try {
    if (mode.value === 'single') {
      const fd = new FormData()
      fd.append('uid', uid)
      fd.append('lang', lang.value)
      fd.append('file', selectedFiles.value[0].file)
      const res = await http.post('/record/upload', fd)
      if (res.code === 200) {
        results.value = [{ index:0, filename: selectedFiles.value[0].file.name,
          status:'ok', result: res.data.result, confidence: res.data.confidence }]
        toast('识别成功')
      } else {
        results.value = [{ index:0, filename: selectedFiles.value[0].file.name, status:'fail', msg: res.msg }]
        toast(res.msg, 'error')
      }
    } else {
      const fd = new FormData()
      fd.append('uid', uid)
      fd.append('lang', lang.value)
      selectedFiles.value.forEach(f => fd.append('files', f.file))
      const res = await http.post('/record/batch_upload', fd)
      if (res.code === 200) {
        results.value = res.data.map((r, i) => ({
          index: i, filename: r.filename, status: r.status,
          result: r.result, confidence: r.confidence, msg: r.msg
        }))
        toast('批量识别完成')
      } else {
        toast(res.msg, 'error')
      }
    }
  } catch(e) {
    toast('请求失败：' + e.message, 'error')
  } finally {
    loading.value = false
  }
}

function copyText(text) {
  navigator.clipboard.writeText(text).then(() => toast('已复制到剪贴板'))
}

function downloadText(text, fname) {
  const a = document.createElement('a')
  a.href = URL.createObjectURL(new Blob([text], { type: 'text/plain;charset=utf-8' }))
  a.download = fname.replace(/\.[^.]+$/, '') + '_ocr.txt'
  a.click()
}
</script>

<style scoped>
.upload-options { display: flex; gap: 16px; margin-bottom: 16px; }
.mode-tabs { display: flex; gap: 0; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; width: fit-content; }
.mode-tab { padding: 8px 24px; border: none; background: #fff; cursor: pointer; font-size: 13px; font-family: inherit; transition: .2s; }
.mode-tab.active { background: var(--primary); color: #fff; }
.file-list { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
.file-item { display: flex; align-items: center; gap: 8px; background: #f8fafc; padding: 6px 10px; border-radius: 8px; border: 1px solid var(--border); }
.file-thumb { width: 40px; height: 40px; object-fit: cover; border-radius: 4px; }
.file-fname { font-size: 12px; color: var(--text-main); max-width: 160px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.result-block { border: 1px solid var(--border); border-radius: 10px; padding: 16px; margin-bottom: 14px; }
.result-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; flex-wrap: wrap; }
.result-fname { font-weight: 600; font-size: 13px; }
.result-text { height: 160px; font-size: 13px; line-height: 1.7; }
</style>

