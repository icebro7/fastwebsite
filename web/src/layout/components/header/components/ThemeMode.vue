<script setup>
import { useAppStore } from '@/store' // 导入应用状态管理
import { useDark, useToggle } from '@vueuse/core' // 导入暗色主题和切换功能

const appStore = useAppStore() // 获取应用状态
const isDark = useDark() // 获取当前是否为暗色主题

const toggleDark = () => {
  appStore.toggleDark() // 切换应用状态中的主题
  useToggle(isDark)() // 切换实际的主题
}
</script>

<template>
  <n-icon mr-20 cursor-pointer size="18" @click="toggleDark">
    <!-- 主题切换图标 -->
    <icon-mdi-moon-waning-crescent v-if="isDark" />
    <icon-mdi-white-balance-sunny v-else />
  </n-icon>
</template>
