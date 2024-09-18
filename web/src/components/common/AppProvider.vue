<!--全局配置 Naive UI 的设置，并将一些 UI 组件的方法挂载到 window 对象上，以便在全局使用。-->

<template>
  <n-config-provider
    wh-full
    :locale="zhCN"
    :date-locale="dateZhCN"
    :theme="appStore.isDark ? darkTheme : undefined"
    :theme-overrides="naiveThemeOverrides"
  >
    <n-loading-bar-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-message-provider>
            <slot></slot>
            <NaiveProviderContent />
          </n-message-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-loading-bar-provider>
  </n-config-provider>
</template>

<script setup>
import { defineComponent, h } from 'vue' // 导入 Vue 3 的 defineComponent 和 h 函数
import {
  zhCN, // 中文语言包
  dateZhCN, // 中文日期格式
  darkTheme, // 暗黑主题
  useLoadingBar, // 加载条钩子函数
  useDialog, // 对话框钩子函数
  useMessage, // 消息钩子函数
  useNotification, // 通知钩子函数
} from 'naive-ui' // 从 Naive UI 导入相关模块
import { useCssVar } from '@vueuse/core' // 从 @vueuse/core 导入 useCssVar 函数
import { kebabCase } from 'lodash-es' // 从 lodash-es 导入 kebabCase 函数
import { setupMessage, setupDialog } from '@/utils' // 从 @/utils 导入 setupMessage 和 setupDialog 函数
import { naiveThemeOverrides } from '~/settings' // 从 ~/settings 导入 naiveThemeOverrides 配置
import { useAppStore } from '@/store' // 从 @/store 导入 useAppStore 函数

const appStore = useAppStore() // 获取应用状态管理

// 设置 CSS 变量
function setupCssVar() {
  const common = naiveThemeOverrides.common // 获取主题覆盖配置中的 common 部分
  for (const key in common) {
    // 遍历 common 对象
    useCssVar(`--${kebabCase(key)}`, document.documentElement).value = common[key] || '' // 将每个键值对转换为 CSS 变量，并设置到 document.documentElement 上
    if (key === 'primaryColor') window.localStorage.setItem('__THEME_COLOR__', common[key] || '') // 如果键是 primaryColor，则将其值存储到 localStorage 中
  }
}

// 挂载 Naive UI 组件的方法至 window 对象，以便在全局使用
function setupNaiveTools() {
  window.$loadingBar = useLoadingBar() // 挂载加载条方法
  window.$notification = useNotification() // 挂载通知方法

  window.$message = setupMessage(useMessage()) // 挂载消息方法，并进行自定义设置
  window.$dialog = setupDialog(useDialog()) // 挂载对话框方法，并进行自定义设置
}

// 定义一个自定义组件，用于设置 CSS 变量和挂载 Naive UI 组件的方法至 window 对象
const NaiveProviderContent = defineComponent({
  setup() {
    setupCssVar() // 调用设置 CSS 变量的函数
    setupNaiveTools() // 调用挂载 Naive UI 组件方法的函数
  },
  render() {
    return h('div') // 返回一个空的 div 元素
  },
})
</script>
