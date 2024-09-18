import axios from 'axios'
import { resReject, resResolve, reqReject, reqResolve } from './interceptors'

// 创建Axios实例的工厂函数
export function createAxios(options = {}) {
  // 默认的Axios配置选项
  const defaultOptions = {
    timeout: 12000, // 请求超时时间设置为12秒
  }

  // 创建Axios实例，合并默认选项和传入的选项
  const service = axios.create({
    ...defaultOptions,
    ...options,
  })

  // 添加请求拦截器
  service.interceptors.request.use(reqResolve, reqReject)

  // 添加响应拦截器
  service.interceptors.response.use(resResolve, resReject)

  // 返回创建的Axios实例
  return service
}

// 创建一个默认的Axios实例，使用VITE_BASE_API作为基础URL
export const request = createAxios({
  baseURL: import.meta.env.VITE_BASE_API, // 从环境变量中获取基础API URL
})
