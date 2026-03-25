<template>
  <router-view />
  <!-- 全局Toast消息 -->
  <div class="toast-wrap">
    <div v-for="t in toasts" :key="t.id" :class="['toast', t.type]">{{ t.msg }}</div>
  </div>
</template>

<script setup>
import { provide, reactive } from 'vue'

// 全局 Toast 系统
const toasts = reactive([])
let tid = 0

function showToast(msg, type = 'success', duration = 3000) {
  const id = ++tid
  toasts.push({ id, msg, type })
  setTimeout(() => {
    const idx = toasts.findIndex(t => t.id === id)
    if (idx !== -1) toasts.splice(idx, 1)
  }, duration)
}

provide('toast', showToast)
</script>

