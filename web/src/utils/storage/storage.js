import { isNullOrUndef } from '@/utils' // 导入判断值是否为null或undefined的工具函数

// Storage类，用于封装存储操作
class Storage {
  constructor(option) {
    this.storage = option.storage // 存储方式（localStorage或sessionStorage）
    this.prefixKey = option.prefixKey // 存储键的前缀
  }

  // 获取带前缀的键
  getKey(key) {
    return `${this.prefixKey}${key}`.toUpperCase()
  }

  // 设置存储项
  set(key, value, expire) {
    const stringData = JSON.stringify({
      value, // 存储的值
      time: Date.now(), // 存储时间
      expire: !isNullOrUndef(expire) ? new Date().getTime() + expire * 1000 : null, // 过期时间
    })
    this.storage.setItem(this.getKey(key), stringData) // 存储数据
  }

  // 获取存储项的值
  get(key) {
    const { value } = this.getItem(key, {})
    return value
  }

  // 获取存储项的详细信息
  getItem(key, def = null) {
    const val = this.storage.getItem(this.getKey(key)) // 获取存储数据
    if (!val) return def // 如果数据不存在，返回默认值
    try {
      const data = JSON.parse(val) // 解析存储数据
      const { value, time, expire } = data
      if (isNullOrUndef(expire) || expire > new Date().getTime()) {
        return { value, time } // 如果未过期，返回存储的值和时间
      }
      this.remove(key) // 如果已过期，移除存储项
      return def // 返回默认值
    } catch (error) {
      this.remove(key) // 解析失败，移除存储项
      return def // 返回默认值
    }
  }

  // 移除存储项
  remove(key) {
    this.storage.removeItem(this.getKey(key))
  }

  // 清空存储
  clear() {
    this.storage.clear()
  }
}

// 创建Storage实例的工厂函数
export function createStorage({ prefixKey = '', storage = sessionStorage }) {
  return new Storage({ prefixKey, storage })
}
