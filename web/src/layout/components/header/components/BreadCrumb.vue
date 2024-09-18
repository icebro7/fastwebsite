<template>
  <n-breadcrumb>
    <!-- 遍历当前路由匹配的路径项 -->
    <n-breadcrumb-item
      v-for="item in route.matched.filter((item) => !!item.meta?.title)"
      :key="item.path"
      @click="handleBreadClick(item.path)"
    >
      <component :is="getIcon(item.meta)" />
      {{ item.meta.title }}
    </n-breadcrumb-item>
  </n-breadcrumb>
</template>

<script setup>
import { renderCustomIcon, renderIcon } from '@/utils' // 导入图标渲染工具函数

const router = useRouter() // 获取路由实例
const route = useRoute() // 获取当前路由信息

function handleBreadClick(path) {
  if (path === route.path) return // 如果点击的是当前路径，则不执行跳转
  router.push(path) // 跳转到指定路径
}

function getIcon(meta) {
  if (meta?.customIcon) return renderCustomIcon(meta.customIcon, { size: 18 }) // 如果有自定义图标，渲染自定义图标
  if (meta?.icon) return renderIcon(meta.icon, { size: 18 }) // 如果有标准图标，渲染标准图标
  return null // 如果没有图标，返回 null
}
</script>
