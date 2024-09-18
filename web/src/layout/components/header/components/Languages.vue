<!--语言切换下拉菜单-->
<template>
  <n-dropdown :options="options" @select="handleChangeLocale">
    <n-icon mr-20 size="18" style="cursor: pointer">
      <icon-mdi:globe />
    </n-icon>
  </n-dropdown>
</template>

<script setup>
import { useI18n } from 'vue-i18n' // 导入国际化功能
import { useAppStore } from '@/store' // 导入应用状态管理
import { router } from '~/src/router' // 导入路由

const store = useAppStore() // 获取应用状态
const { availableLocales, t } = useI18n() // 使用国际化功能

const options = computed(() => {
  let select = []
  availableLocales.forEach((locale) => {
    select.push({
      label: t('lang', 1, { locale: locale }), // 根据当前语言显示语言名称
      key: locale, // 语言键值
    })
  })
  return select
})

const handleChangeLocale = (value) => {
  store.setLocale(value) // 设置新的语言
  // 重新加载页面
  router.go()
}
</script>
