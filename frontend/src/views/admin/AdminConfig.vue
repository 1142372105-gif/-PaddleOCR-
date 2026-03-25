<template>
  <div>
    <div class="page-title">🔧 系统配置</div>

    <div class="card">
      <div class="config-tip">
        <span>⚠️</span>
        <span>系统配置修改后立即生效，请谨慎操作。OCR参数变更将影响后续识别结果。</span>
      </div>

      <table class="data-table" style="margin-top:16px">
        <thead>
          <tr>
            <th style="width:180px">配置键名</th>
            <th style="width:200px">配置值</th>
            <th>说明</th>
            <th>最后更新</th>
            <th style="width:80px">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in configs" :key="c.id">
            <td><code class="cfg-key">{{ c.cfgkey }}</code></td>
            <td>
              <input
                v-if="editing===c.id"
                class="form-input"
                style="padding:4px 8px;font-size:12px"
                v-model="c.cfgval"
              />
              <span v-else class="cfg-val">{{ c.cfgval }}</span>
            </td>
            <td class="cfg-remark">{{ c.remark }}</td>
            <td style="font-size:12px;color:var(--text-sub)">{{ c.updatedat }}</td>
            <td>
              <div style="display:flex;gap:5px">
                <button v-if="editing!==c.id" class="btn btn-outline btn-sm" @click="editing=c.id">编辑</button>
                <button v-else class="btn btn-success btn-sm" @click="saveConfig(c)">保存</button>
                <button v-if="editing===c.id" class="btn btn-outline btn-sm" @click="editing=null;load()">取消</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 配置说明卡片 -->
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px;margin-top:20px">
      <div class="card cfg-card" v-for="tip in cfgTips" :key="tip.key">
        <div class="cfg-card-icon">{{ tip.icon }}</div>
        <div class="cfg-card-key">{{ tip.key }}</div>
        <div class="cfg-card-desc">{{ tip.desc }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, inject } from 'vue'
import http from '../../http'

const toast = inject('toast')
const configs = ref([])
const editing = ref(null)

const cfgTips = [
  { icon: '🌐', key: 'ocr.lang',      desc: '默认识别语言代码，如 ch/en/japan' },
  { icon: '🎯', key: 'ocr.threshold', desc: '文本检测置信度阈值，0~1之间，越高越严格' },
  { icon: '🔄', key: 'ocr.useangle',  desc: '是否启用文字方向分类，1开启 0关闭' },
  { icon: '📦', key: 'ocr.maxsize',   desc: '单张图片最大上传尺寸（MB）' },
  { icon: '📁', key: 'ocr.batchmax',  desc: '批量上传一次最多允许的图片数量' },
  { icon: '🏷️', key: 'sys.title',     desc: '系统名称，显示在页面标题区域' }
]

async function load() {
  const res = await http.get('/admin/config/list')
  if (res.code === 200) configs.value = res.data
}
onMounted(load)

async function saveConfig(c) {
  const res = await http.post('/admin/config/update', { id: c.id, cfgval: c.cfgval })
  if (res.code === 200) {
    toast('配置已更新')
    editing.value = null
    load()
  } else {
    toast(res.msg, 'error')
  }
}
</script>

<style scoped>
.config-tip {
  display: flex; align-items: center; gap: 10px;
  background: #fef9c3; border: 1px solid #fde68a; border-radius: 8px;
  padding: 12px 16px; font-size: 13px; color: #92400e;
}
.cfg-key { background: #f1f5f9; padding: 2px 8px; border-radius: 4px; font-size: 12px; color: var(--primary); }
.cfg-val { font-size: 13px; font-weight: 500; }
.cfg-remark { font-size: 12px; color: var(--text-sub); }

.cfg-card { display: flex; flex-direction: column; gap: 6px; }
.cfg-card-icon { font-size: 24px; }
.cfg-card-key { font-size: 12px; font-weight: 700; color: var(--primary); font-family: monospace; }
.cfg-card-desc { font-size: 12px; color: var(--text-sub); line-height: 1.5; }
</style>

