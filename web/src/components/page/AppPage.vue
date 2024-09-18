<template>
  <!-- 使用过渡效果，过渡名称为 fade-slide，模式为 out-in，初次渲染时也应用过渡效果 -->
  <transition name="fade-slide" mode="out-in" appear>
    <!-- 主要内容区域，可垂直滚动，全屏显示，背景颜色为 #f5f6fb，暗黑模式下为 #121212，内边距为 15px -->
    <section class="cus-scroll-y wh-full flex-col bg-[#f5f6fb] p-15 dark:bg-hex-121212">
      <!-- 插槽，用于插入子组件 -->
      <slot />
      <!-- 如果 showFooter 为 true，显示 AppFooter 组件，下方留出 15px 的间距 -->
      <AppFooter v-if="showFooter" class="mt-15" />
      <!-- 返回顶部按钮，距离底部 20px -->
      <n-back-top :bottom="20" />
    </section>
  </transition>
</template>

<script setup>
// 定义组件的 props，接收一个布尔类型的 showFooter，默认值为 false
defineProps({
  showFooter: {
    type: Boolean,
    default: false,
  },
})
</script>
