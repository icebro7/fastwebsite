import { getToken } from '@/utils' // 导入获取token的工具函数
import { resolveResError } from './helpers' // 导入处理响应错误的辅助函数
import { useUserStore } from '@/store' // 导入用户状态管理

// 请求拦截器：处理请求配置
export function reqResolve(config) {
  // 处理不需要token的请求
  if (config.noNeedToken) {
    return config
  }

  const token = getToken() // 获取token
  if (token) {
    // 如果请求头中没有token，则添加token
    config.headers.token = config.headers.token || token
  }

  return config // 返回处理后的配置
}

// 请求拦截器：处理请求错误
export function reqReject(error) {
  return Promise.reject(error) // 直接返回错误
}

// 响应拦截器：处理响应成功
export function resResolve(response) {
  const { data, status, statusText } = response // 解构响应数据
  if (data?.code !== 200) {
    const code = data?.code ?? status // 获取错误码
    /** 根据code处理对应的操作，并返回处理后的message */
    const message = resolveResError(code, data?.msg ?? statusText)
    window.$message?.error(message, { keepAliveOnHover: true }) // 显示错误消息
    return Promise.reject({ code, message, error: data || response }) // 返回错误
  }
  return Promise.resolve(data) // 返回成功数据
}

// 响应拦截器：处理响应错误
export async function resReject(error) {
  if (!error || !error.response) {
    const code = error?.code // 获取错误码
    /** 根据code处理对应的操作，并返回处理后的message */
    const message = resolveResError(code, error.message)
    window.$message?.error(message) // 显示错误消息
    return Promise.reject({ code, message, error }) // 返回错误
  }
  const { data, status } = error.response // 解构响应数据

  if (data?.code === 401) {
    try {
      const userStore = useUserStore() // 获取用户状态管理实例
      userStore.logout() // 执行登出操作
    } catch (error) {
      console.log('resReject error', error) // 捕获并记录错误
      return
    }
  }
  // 后端返回的response数据
  const code = data?.code ?? status // 获取错误码
  const message = resolveResError(code, data?.msg ?? error.message) // 处理错误消息
  window.$message?.error(message, { keepAliveOnHover: true }) // 显示错误消息
  return Promise.reject({ code, message, error: error.response?.data || error.response }) // 返回错误
}
