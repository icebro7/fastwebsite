<!--实现了一个路由视图，使用 KeepAlive 组件来缓存路由组件，以提高性能-->
<template>
  <router-view v-slot="{ Component, route }">
    <KeepAlive :include="keepAliveRouteNames">
      <component
        :is="Component"
        v-if="appStore.reloadFlag"
        :key="appStore.aliveKeys[route.name] || route.fullPath"
      />
    </KeepAlive>
  </router-view>
</template>

<script setup>
import { useAppStore } from '@/store' // 导入应用状态管理
import { useRouter } from 'vue-router' // 导入路由
const appStore = useAppStore() // 获取应用状态
const router = useRouter() // 获取路由实例

const allRoutes = router.getRoutes() // 获取所有路由
const keepAliveRouteNames = computed(() => {
  return allRoutes.filter((route) => route.meta?.keepAlive).map((route) => route.name) // 过滤并获取需要缓存的路由名称
})
</script>
