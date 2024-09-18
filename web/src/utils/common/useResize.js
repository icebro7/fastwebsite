// 导出一个用于监听元素尺寸变化的函数
export function useResize(el, cb) {
  // 创建一个 ResizeObserver 实例，用于监听元素尺寸变化
  const observer = new ResizeObserver((entries) => {
    // 当元素尺寸变化时，调用回调函数，并传入元素的内容矩形区域
    cb(entries[0].contentRect)
  })
  // 开始监听指定元素的尺寸变化
  observer.observe(el)
  // 返回 observer 实例，以便在需要时停止监听
  return observer
}

// 定义一个安装函数，用于将自定义指令注册到 Vue 应用中
const install = (app) => {
  let observer // 定义一个变量，用于存储 ResizeObserver 实例

  // 注册一个名为 'resize' 的自定义指令
  app.directive('resize', {
    // 当指令绑定到元素时调用
    mounted(el, binding) {
      // 使用 useResize 函数监听元素的尺寸变化，并将回调函数绑定到指令的值
      observer = useResize(el, binding.value)
    },
    // 当指令从元素上解绑时调用
    beforeUnmount() {
      // 停止监听元素的尺寸变化
      observer?.disconnect()
    },
  })
}

// 将 install 函数绑定到 useResize 函数上，以便可以通过 useResize.install 调用
useResize.install = install
