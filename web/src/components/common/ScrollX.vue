<!--创建一个可滚动的容器，支持鼠标滚轮滚动和箭头按钮控制滚动-->

<template>
  <div ref="wrapper" class="wrapper" @mousewheel.prevent="handleMouseWheel">
    <template v-if="showArrow && isOverflow">
      <div class="left" @click="handleMouseWheel({ wheelDelta: 120 })">
        <icon-ic:baseline-keyboard-arrow-left />
      </div>
      <div class="right" @click="handleMouseWheel({ wheelDelta: -120 })">
        <icon-ic:baseline-keyboard-arrow-right />
      </div>
    </template>

    <div
      ref="content"
      v-resize="refreshIsOverflow"
      class="content"
      :class="{ overflow: isOverflow && showArrow }"
      :style="{
        transform: `translateX(${translateX}px)`,
      }"
    >
      <slot />
    </div>
  </div>
</template>

<script setup>
import { debounce, useResize } from '@/utils' // 导入工具函数

// 定义组件的 props
defineProps({
  showArrow: {
    type: Boolean,
    default: true,
  },
})

// 定义响应式变量
const translateX = ref(0) // 内容平移的距离
const content = ref(null) // 内容 div 的引用
const wrapper = ref(null) // 容器 div 的引用
const isOverflow = ref(false) // 内容是否溢出

// 防抖函数，用于刷新内容是否溢出
const refreshIsOverflow = debounce(() => {
  const wrapperWidth = wrapper.value?.offsetWidth // 容器的宽度
  const contentWidth = content.value?.offsetWidth // 内容的宽度
  isOverflow.value = contentWidth > wrapperWidth // 判断内容是否溢出
  resetTranslateX(wrapperWidth, contentWidth) // 重置平移距离
}, 200)

// 处理鼠标滚轮事件
function handleMouseWheel(e) {
  const { wheelDelta } = e // 获取滚轮滚动值
  const wrapperWidth = wrapper.value?.offsetWidth // 容器的宽度
  const contentWidth = content.value?.offsetWidth // 内容的宽度
  /**
   * @wheelDelta 平行滚动的值 >0： 右移  <0: 左移
   * @translateX 内容translateX的值
   * @wrapperWidth 容器的宽度
   * @contentWidth 内容的宽度
   */
  if (wheelDelta < 0) {
    // 如果内容宽度小于容器宽度且平移距离小于 -10，则不处理
    if (wrapperWidth > contentWidth && translateX.value < -10) return
    // 如果内容宽度大于容器宽度且内容宽度加上平移距离减去容器宽度小于 -10，则不处理
    if (wrapperWidth <= contentWidth && contentWidth + translateX.value - wrapperWidth < -10) return
  }
  // 如果滚轮滚动值大于 0 且平移距离大于 10，则不处理
  if (wheelDelta > 0 && translateX.value > 10) {
    return
  }

  translateX.value += wheelDelta // 更新平移距离
  resetTranslateX(wrapperWidth, contentWidth) // 重置平移距离
}

// 防抖函数，用于重置平移距离
const resetTranslateX = debounce(function (wrapperWidth, contentWidth) {
  if (!isOverflow.value) {
    // 如果内容没有溢出，平移距离设为 0
    translateX.value = 0
  } else if (-translateX.value > contentWidth - wrapperWidth) {
    // 如果平移距离超过内容宽度减去容器宽度，则平移距离设为容器宽度减去内容宽度
    translateX.value = wrapperWidth - contentWidth
  } else if (translateX.value > 0) {
    // 如果平移距离大于 0，则平移距离设为 0
    translateX.value = 0
  }
}, 200)

// 定义观察者变量
const observer = ref(null)
onMounted(() => {
  refreshIsOverflow() // 刷新内容是否溢出

  observer.value = useResize(document.body, refreshIsOverflow) // 监听 body 的 resize 事件
})
onBeforeUnmount(() => {
  observer.value?.disconnect() // 组件卸载时断开观察者
})

// 处理滚动事件
function handleScroll(x, width) {
  const wrapperWidth = wrapper.value?.offsetWidth // 容器的宽度
  const contentWidth = content.value?.offsetWidth // 内容的宽度
  if (contentWidth <= wrapperWidth) return // 如果内容宽度小于等于容器宽度，则不处理

  // 当 x 小于可视范围的最小值时
  if (x < -translateX.value + 150) {
    translateX.value = -(x - 150) // 更新平移距离
    resetTranslateX(wrapperWidth, contentWidth) // 重置平移距离
  }

  // 当 x 大于可视范围的最大值时
  if (x + width > -translateX.value + wrapperWidth) {
    translateX.value = wrapperWidth - (x + width) // 更新平移距离
    resetTranslateX(wrapperWidth, contentWidth) // 重置平移距离
  }
}

// 暴露 handleScroll 方法
defineExpose({
  handleScroll,
})
</script>

<style lang="scss" scoped>
.wrapper {
  display: flex;
  background-color: #fff;

  z-index: 9;
  overflow: hidden;
  position: relative;
  .content {
    padding: 0 10px;
    display: flex;
    align-items: center;
    flex-wrap: nowrap;
    transition: transform 0.5s;
    &.overflow {
      padding-left: 30px;
      padding-right: 30px;
    }
  }
  .left,
  .right {
    background-color: #fff;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;

    width: 20px;
    height: 35px;
    display: flex;
    align-items: center;
    justify-content: center;

    font-size: 18px;
    border: 1px solid #e0e0e6;
    border-radius: 2px;

    z-index: 2;
    cursor: pointer;
  }
  .left {
    left: 0;
  }
  .right {
    right: 0;
  }
}
</style>
