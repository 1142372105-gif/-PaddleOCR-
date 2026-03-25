<template>
  <div>
    <div class="page-title">❓ 帮助中心</div>

    <!-- 标签切换 -->
    <div class="help-tabs">
      <button :class="['help-tab',tab==='tutorial'?'active':'']" @click="tab='tutorial'">📖 使用教程</button>
      <button :class="['help-tab',tab==='faq'?'active':'']" @click="tab='faq'">💬 常见问题</button>
      <button :class="['help-tab',tab==='contact'?'active':'']" @click="tab='contact'">📞 联系支持</button>
    </div>

    <!-- 使用教程 -->
    <div v-if="tab==='tutorial'" class="card">
      <div class="tut-step" v-for="s in steps" :key="s.step">
        <div class="tut-num">{{ s.step }}</div>
        <div class="tut-content">
          <div class="tut-title">{{ s.title }}</div>
          <div class="tut-desc">{{ s.desc }}</div>
        </div>
      </div>
    </div>

    <!-- 常见问题 -->
    <div v-if="tab==='faq'" class="card">
      <div class="faq-item" v-for="(q,i) in faqs" :key="i">
        <div class="faq-q" @click="toggleFaq(i)">
          <span>{{ q.q }}</span>
          <span class="faq-arrow">{{ q.open ? '▲' : '▼' }}</span>
        </div>
        <div v-show="q.open" class="faq-a">{{ q.a }}</div>
      </div>
    </div>

    <!-- 联系支持 -->
    <div v-if="tab==='contact'" class="card">
      <div class="contact-list">
        <div class="contact-item">
          <div class="ci-icon">📧</div>
          <div class="ci-info">
            <div class="ci-name">技术支持邮箱</div>
            <div class="ci-val">support@ocrtest.com</div>
          </div>
        </div>
        <div class="contact-item">
          <div class="ci-icon">💻</div>
          <div class="ci-info">
            <div class="ci-name">官方文档</div>
            <div class="ci-val">https://github.com/PaddlePaddle/PaddleOCR</div>
          </div>
        </div>
        <div class="contact-item">
          <div class="ci-icon">🕐</div>
          <div class="ci-info">
            <div class="ci-name">服务时间</div>
            <div class="ci-val">工作日 09:00 ~ 18:00</div>
          </div>
        </div>
      </div>
      <div class="card" style="margin-top:16px;background:var(--bg)">
        <div class="section-title">提交反馈</div>
        <div class="form-group">
          <label>问题描述</label>
          <textarea class="form-textarea" v-model="feedback" placeholder="请描述您遇到的问题..." />
        </div>
        <button class="btn btn-primary" @click="submitFeedback">提交反馈</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, inject } from 'vue'

const toast = inject('toast')
const tab = ref('tutorial')
const feedback = ref('')

const steps = [
  { step: 1, title: '注册/登录账号', desc: '点击首页"注册新账号"按钮，填写用户名、密码及安全问题完成注册。已有账号直接输入用户名密码登录。' },
  { step: 2, title: '上传图片', desc: '进入"图片识别"页面，可单张上传或批量上传。支持点击选择文件或直接拖拽图片到上传区域。' },
  { step: 3, title: '选择识别语言', desc: '在上传前选择图片对应的文字语言，系统支持中文、英文、日语等10种语言。' },
  { step: 4, title: '开始识别', desc: '上传完成后点击"开始识别"按钮，系统将使用PP-OCRv3引擎自动检测并识别图片中的文字。' },
  { step: 5, title: '查看与编辑结果', desc: '识别完成后可以直接查看、编辑结果文本，也可以复制或导出为TXT文件。' },
  { step: 6, title: '历史记录管理', desc: '所有识别记录保存在"识别历史"中，支持查看详情、编辑结果、导出文本及删除记录。' }
]

const faqs = reactive([
  { q: '支持哪些图片格式？', a: '支持 PNG、JPG/JPEG、BMP、TIFF、WEBP 等常见图片格式，单张最大10MB。', open: false },
  { q: '识别准确率如何？', a: 'PP-OCRv3在印刷文本识别方面准确率超90%，手写文字和模糊图片识别率会有所下降，建议上传清晰图片。', open: false },
  { q: '如何忘记密码找回账号？', a: '点击登录页"忘记密码"，输入用户名后回答注册时设置的安全问题，回答正确即可重置密码。', open: false },
  { q: '批量上传有数量限制吗？', a: '批量上传默认最多20张，具体以管理员配置为准。', open: false },
  { q: '识别失败怎么办？', a: '请检查图片是否清晰、文字是否清楚，确认选择了正确的识别语言，然后重新上传尝试。', open: false },
  { q: '识别结果可以修改吗？', a: '可以！在识别历史页面点击"详情"，文本区域支持直接编辑，修改后点击"保存修改"即可。', open: false }
])

function toggleFaq(i) { faqs[i].open = !faqs[i].open }

function submitFeedback() {
  if (!feedback.value.trim()) { toast('请填写反馈内容', 'warning'); return }
  toast('反馈已提交，感谢您的建议！')
  feedback.value = ''
}
</script>

<style scoped>
.help-tabs { display: flex; gap: 8px; margin-bottom: 16px; }
.help-tab { padding: 9px 22px; border: 1px solid var(--border); background: #fff; border-radius: 8px; cursor: pointer; font-size: 13px; font-family: inherit; transition: .2s; }
.help-tab.active { background: var(--primary); color: #fff; border-color: var(--primary); }
.tut-step { display: flex; gap: 16px; padding: 16px 0; border-bottom: 1px solid var(--border); }
.tut-step:last-child { border-bottom: none; }
.tut-num { width: 32px; height: 32px; background: var(--primary); color: #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; flex-shrink: 0; }
.tut-title { font-weight: 600; font-size: 14px; margin-bottom: 4px; }
.tut-desc { font-size: 13px; color: var(--text-sub); line-height: 1.7; }
.faq-item { border-bottom: 1px solid var(--border); }
.faq-q { display: flex; justify-content: space-between; align-items: center; padding: 14px 0; cursor: pointer; font-weight: 500; font-size: 13px; }
.faq-q:hover { color: var(--primary); }
.faq-arrow { font-size: 11px; color: var(--text-sub); }
.faq-a { padding: 0 0 14px; font-size: 13px; color: var(--text-sub); line-height: 1.7; }
.contact-list { display: flex; flex-direction: column; gap: 0; }
.contact-item { display: flex; align-items: center; gap: 14px; padding: 16px 0; border-bottom: 1px solid var(--border); }
.ci-icon { font-size: 24px; width: 40px; text-align: center; }
.ci-name { font-size: 12px; color: var(--text-sub); margin-bottom: 3px; }
.ci-val { font-size: 13px; font-weight: 500; }
.section-title { font-size: 14px; font-weight: 600; margin-bottom: 12px; }
</style>

