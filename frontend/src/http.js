// axios封装：统一处理请求和响应
import axios from 'axios'

const http = axios.create({
  baseURL: '/api',
  timeout: 60000,   // OCR识别较耗时，超时设60秒
  withCredentials: true
})

// 响应拦截器
http.interceptors.response.use(
  res => res.data,
  err => {
    console.error('[请求错误]', err)
    return Promise.reject(err)
  }
)

export default http

