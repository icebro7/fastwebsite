<template>
  <n-dropdown :options="options" @select="handleSelect">
    <!-- 用户菜单下拉框 -->
    <div flex cursor-pointer items-center>
      <!-- 用户名显示区域 -->
      <span>{{ userStore.name }}</span>
    </div>
  </n-dropdown>
</template>

<script setup>
import { useUserStore } from '@/store' // 导入用户状态管理
import { renderIcon } from '@/utils' // 导入图标渲染工具
import { useRouter } from 'vue-router' // 导入路由
import { useI18n } from 'vue-i18n' // 导入国际化

const { t } = useI18n() // 获取国际化翻译方法

const router = useRouter() // 获取路由实例

const userStore = useUserStore() // 获取用户状态

const options = [
  {
    label: t('header.label_profile'), // 个人资料菜单项
    key: 'profile',
    icon: renderIcon('mdi-account-arrow-right-outline', { size: '14px' }), // 个人资料图标
  },
  {
    label: t('header.label_logout'), // 登出菜单项
    key: 'logout',
    icon: renderIcon('mdi:exit-to-app', { size: '14px' }), // 登出图标
  },
]

function handleSelect(key) {
  if (key === 'profile') {
    router.push('/profile') // 跳转到个人资料页面
  } else if (key === 'logout') {
    $dialog.confirm({
      title: t('header.label_logout_dialog_title'), // 登出确认对话框标题
      type: 'warning',
      content: t('header.text_logout_confirm'), // 登出确认对话框内容
      confirm() {
        userStore.logout() // 执行登出操作
        $message.success(t('header.text_logout_success')) // 显示登出成功消息
      },
    })
  }
}
</script>
