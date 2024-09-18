// 类型判断和值验证的工具函数

const toString = Object.prototype.toString // 获取对象的原型方法 toString

// 判断值的类型是否为指定类型
export function is(val, type) {
  return toString.call(val) === `[object ${type}]`
}

// 判断值是否已定义
export function isDef(val) {
  return typeof val !== 'undefined'
}

// 判断值是否未定义
export function isUndef(val) {
  return typeof val === 'undefined'
}

// 判断值是否为 null
export function isNull(val) {
  return val === null
}

// 判断值是否为空字符串
export function isWhitespace(val) {
  return val === ''
}

// 判断值是否为对象
export function isObject(val) {
  return !isNull(val) && is(val, 'Object')
}

// 判断值是否为数组
export function isArray(val) {
  return val && Array.isArray(val)
}

// 判断值是否为字符串
export function isString(val) {
  return is(val, 'String')
}

// 判断值是否为数字
export function isNumber(val) {
  return is(val, 'Number')
}

// 判断值是否为布尔值
export function isBoolean(val) {
  return is(val, 'Boolean')
}

// 判断值是否为日期对象
export function isDate(val) {
  return is(val, 'Date')
}

// 判断值是否为正则表达式
export function isRegExp(val) {
  return is(val, 'RegExp')
}

// 判断值是否为函数
export function isFunction(val) {
  return typeof val === 'function'
}

// 判断值是否为 Promise
export function isPromise(val) {
  return is(val, 'Promise') && isObject(val) && isFunction(val.then) && isFunction(val.catch)
}

// 判断值是否为 DOM 元素
export function isElement(val) {
  return isObject(val) && !!val.tagName
}

// 判断值是否为 Window 对象
export function isWindow(val) {
  return typeof window !== 'undefined' && isDef(window) && is(val, 'Window')
}

// 判断值是否为 null 或未定义
export function isNullOrUndef(val) {
  return isNull(val) || isUndef(val)
}

// 判断值是否为 null、未定义或空字符串
export function isNullOrWhitespace(val) {
  return isNullOrUndef(val) || isWhitespace(val)
}

/** 判断值是否为空数组、空字符串、空对象、空 Map 或空 Set */
export function isEmpty(val) {
  if (isArray(val) || isString(val)) {
    return val.length === 0
  }

  if (val instanceof Map || val instanceof Set) {
    return val.size === 0
  }

  if (isObject(val)) {
    return Object.keys(val).length === 0
  }

  return false
}

/**
 * * 类似 MySQL 的 IFNULL 函数
 * * 如果第一个参数为 null、未定义或空字符串，则返回第二个参数作为备用值，否则返回第一个参数
 * @param {Number|Boolean|String} val
 * @param {Number|Boolean|String} def
 * @returns
 */
export function ifNull(val, def = '') {
  return isNullOrWhitespace(val) ? def : val
}

// 判断路径是否为 URL
export function isUrl(path) {
  const reg =
    /(((^https?:(?:\/\/)?)(?:[-;:&=+$,\w]+@)?[A-Za-z0-9.-]+(?::\d+)?|(?:www.|[-;:&=+$,\w]+@)[A-Za-z0-9.-]+)((?:\/[+~%/.\w-_]*)?\??(?:[-+=&;%@.\w_]*)#?(?:[\w]*))?)$/
  return reg.test(path)
}

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

// 判断是否为服务器环境
export const isServer = typeof window === 'undefined'

// 判断是否为客户端环境
export const isClient = !isServer
