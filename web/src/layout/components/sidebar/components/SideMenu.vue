<!--侧边栏菜单，根据用户的权限动态生成菜单项-->
<template>
  <n-menu
    ref="menu"
    class="side-menu"
    accordion
    :indent="18"
    :collapsed-icon-size="22"
    :collapsed-width="64"
    :options="menuOptions"
    :value="activeKey"
    @update:value="handleMenuSelect"
  />
</template>

<script setup>
import { usePermissionStore, useAppStore } from '@/store' // 导入权限和应用状态管理
import { renderCustomIcon, renderIcon, isExternal } from '@/utils' // 导入图标渲染和外部链接判断工具

const router = useRouter() // 获取路由实例
const curRoute = useRoute() // 获取当前路由信息
const permissionStore = usePermissionStore() // 获取权限状态
const appStore = useAppStore() // 获取应用状态

const activeKey = computed(() => curRoute.meta?.activeMenu || curRoute.name) // 计算当前激活的菜单项

const menuOptions = computed(() => {
  return permissionStore.menus.map((item) => getMenuItem(item)).sort((a, b) => a.order - b.order) // 生成菜单项并排序
})

const menu = ref(null) // 菜单组件实例
watch(curRoute, async () => {
  await nextTick()
  menu.value?.showOption() // 监听路由变化，更新菜单项
})

function resolvePath(basePath, path) {
  if (isExternal(path)) return path // 判断是否为外部链接
  return (
    '/' +
    [basePath, path]
      .filter((path) => !!path && path !== '/')
      .map((path) => path.replace(/(^\/)|(\/$)/g, ''))
      .join('/')
  ) // 解析路径
}

function getMenuItem(route, basePath = '') {
  let menuItem = {
    label: (route.meta && route.meta.title) || route.name, // 菜单项标签
    key: route.name, // 菜单项键值
    path: resolvePath(basePath, route.path), // 菜单项路径
    icon: getIcon(route.meta), // 菜单项图标
    order: route.meta?.order || 0, // 菜单项顺序
  }

  const visibleChildren = route.children
    ? route.children.filter((item) => item.name && !item.isHidden) // 过滤可见子路由
    : []

  if (!visibleChildren.length) return menuItem // 如果没有可见子路由，返回菜单项

  if (visibleChildren.length === 1) {
    // 单个子路由处理
    const singleRoute = visibleChildren[0]
    menuItem = {
      ...menuItem,
      label: singleRoute.meta?.title || singleRoute.name,
      key: singleRoute.name,
      path: resolvePath(menuItem.path, singleRoute.path),
      icon: getIcon(singleRoute.meta),
    }
    const visibleItems = singleRoute.children
      ? singleRoute.children.filter((item) => item.name && !item.isHidden)
      : []

    if (visibleItems.length === 1) {
      menuItem = getMenuItem(visibleItems[0], menuItem.path)
    } else if (visibleItems.length > 1) {
      menuItem.children = visibleItems
        .map((item) => getMenuItem(item, menuItem.path))
        .sort((a, b) => a.order - b.order)
    }
  } else {
    menuItem.children = visibleChildren
      .map((item) => getMenuItem(item, menuItem.path))
      .sort((a, b) => a.order - b.order)
  }
  return menuItem
}

function getIcon(meta) {
  if (meta?.customIcon) return renderCustomIcon(meta.customIcon, { size: 18 }) // 自定义图标
  if (meta?.icon) return renderIcon(meta.icon, { size: 18 }) // 标准图标
  return null
}

function handleMenuSelect(key, item) {
  if (isExternal(item.path)) {
    window.open(item.path) // 外部链接跳转
  } else {
    if (item.path === curRoute.path) {
      appStore.reloadPage() // 刷新页面
    } else {
      router.push(item.path) // 路由跳转
    }
  }
}
</script>

<style lang="scss">
.side-menu:not(.n-menu--collapsed) {
  .n-menu-item-content {
    &::before {
      left: 5px;
      right: 5px;
    }
    &.n-menu-item-content--selected,
    &:hover {
      &::before {
        border-left: 4px solid var(--primary-color);
      }
    }
  }
}
</style>
