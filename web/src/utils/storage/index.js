import { createStorage } from './storage' // 导入创建存储的工厂函数

const prefixKey = '' // 定义存储键的前缀

// 创建本地存储实例的工厂函数
export const createLocalStorage = function (option = {}) {
  return createStorage({
    prefixKey: option.prefixKey || '', // 使用传入的前缀键或默认空字符串
    storage: localStorage, // 使用浏览器的localStorage
  })
}

// 创建会话存储实例的工厂函数
export const createSessionStorage = function (option = {}) {
  return createStorage({
    prefixKey: option.prefixKey || '', // 使用传入的前缀键或默认空字符串
    storage: sessionStorage, // 使用浏览器的sessionStorage
  })
}

// 创建本地存储实例，使用默认的前缀键
export const lStorage = createLocalStorage({ prefixKey })

// 创建会话存储实例，使用默认的前缀键
export const sStorage = createSessionStorage({ prefixKey })
