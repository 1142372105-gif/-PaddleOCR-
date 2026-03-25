// 全局状态：用户登录信息（用localStorage持久化）
import { reactive } from 'vue'

export const store = reactive({
  user: JSON.parse(localStorage.getItem('ocr_user') || 'null'),

  setUser(u) {
    this.user = u
    if (u) localStorage.setItem('ocr_user', JSON.stringify(u))
    else localStorage.removeItem('ocr_user')
  },

  isAdmin() {
    return this.user && this.user.role === 1
  },

  isLogin() {
    return !!this.user
  }
})

