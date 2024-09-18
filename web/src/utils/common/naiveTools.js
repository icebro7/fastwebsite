import { isNullOrUndef } from '@/utils' // 导入工具函数，用于判断值是否为 null 或未定义

// 消息管理工具
export function setupMessage(NMessage) {
  let loadingMessage = null // 存储当前正在显示的 loading 消息

  class Message {
    /**
     * 规则：
     * * loading message 只显示一个，新的 message 会替换正在显示的 loading message
     * * loading message 不会自动清除，除非被替换成非 loading message，非 loading message 默认 2 秒后自动清除
     */

    // 移除消息
    removeMessage(message = loadingMessage, duration = 2000) {
      setTimeout(() => {
        if (message) {
          message.destroy() // 销毁消息
          message = null // 清空消息引用
        }
      }, duration)
    }

    // 显示消息
    showMessage(type, content, option = {}) {
      if (loadingMessage && loadingMessage.type === 'loading') {
        // 如果存在则替换正在显示的 loading message
        loadingMessage.type = type
        loadingMessage.content = content

        if (type !== 'loading') {
          // 非 loading message 需设置自动清除
          this.removeMessage(loadingMessage, option.duration)
        }
      } else {
        // 不存在正在显示的 loading 则新建一个 message, 如果新建的 message 是 loading message 则将 message 赋值存储下来
        let message = NMessage[type](content, option)
        if (type === 'loading') {
          loadingMessage = message
        }
      }
    }

    // 显示 loading 消息
    loading(content) {
      this.showMessage('loading', content, { duration: 0 })
    }

    // 显示成功消息
    success(content, option = {}) {
      this.showMessage('success', content, option)
    }

    // 显示错误消息
    error(content, option = {}) {
      this.showMessage('error', content, option)
    }

    // 显示信息消息
    info(content, option = {}) {
      this.showMessage('info', content, option)
    }

    // 显示警告消息
    warning(content, option = {}) {
      this.showMessage('warning', content, option)
    }
  }

  return new Message() // 返回 Message 类的实例
}

// 对话框管理工具
export function setupDialog(NDialog) {
  // 扩展 NDialog 的 confirm 方法
  NDialog.confirm = function (option = {}) {
    const showIcon = !isNullOrUndef(option.title) // 判断是否显示图标
    return NDialog[option.type || 'warning']({
      showIcon, // 是否显示图标
      positiveText: '确定', // 确定按钮文本
      negativeText: '取消', // 取消按钮文本
      onPositiveClick: option.confirm, // 确定按钮点击事件
      onNegativeClick: option.cancel, // 取消按钮点击事件
      onMaskClick: option.cancel, // 遮罩点击事件
      ...option, // 其他选项
    })
  }

  return NDialog // 返回扩展后的 NDialog
}
