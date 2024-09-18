import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import { setupRouterGuard } from './guard'
import { basicRoutes, EMPTY_ROUTE, NOT_FOUND_ROUTE } from './routes'
import { getToken, isNullOrWhitespace } from '@/utils'
import { useUserStore, usePermissionStore } from '@/store'

// 根据环境变量判断是否使用 hash 模式
const isHash = import.meta.env.VITE_USE_HASH === 'true'
// 创建路由实例，设置历史模式、基础路由和滚动行为
export const router = createRouter({
  history: isHash ? createWebHashHistory('/') : createWebHistory('/'),
  routes: basicRoutes,
  scrollBehavior: () => ({ left: 0, top: 0 }),
})

// 设置路由的函数，包括添加动态路由、设置路由守卫和使用路由实例。
export async function setupRouter(app) {
  await addDynamicRoutes()
  setupRouterGuard(router)
  app.use(router)
}

// 重置路由的函数，移除所有非基础路由
export async function resetRouter() {
  const basicRouteNames = getRouteNames(basicRoutes)
  router.getRoutes().forEach((route) => {
    const name = route.name
    if (!basicRouteNames.includes(name)) {
      router.removeRoute(name)
    }
  })
}

export async function addDynamicRoutes() {
  const token = getToken()

  // 没有token情况
  if (isNullOrWhitespace(token)) {
    router.addRoute(EMPTY_ROUTE)
    return
  }
  // 有token的情况
  const userStore = useUserStore()
  const permissionStore = usePermissionStore()
  !userStore.userId && (await userStore.getUserInfo())
  try {
    const accessRoutes = await permissionStore.generateRoutes()
    await permissionStore.getAccessApis()
    accessRoutes.forEach((route) => {
      !router.hasRoute(route.name) && router.addRoute(route)
    })
    router.hasRoute(EMPTY_ROUTE.name) && router.removeRoute(EMPTY_ROUTE.name)
    router.addRoute(NOT_FOUND_ROUTE)
  } catch (error) {
    console.error('error', error)
    const userStore = useUserStore()
    await userStore.logout()
  }
}

export function getRouteNames(routes) {
  return routes.map((route) => getRouteName(route)).flat(1)
}

function getRouteName(route) {
  const names = [route.name]
  if (route.children && route.children.length) {
    names.push(...route.children.map((item) => getRouteName(item)).flat(1))
  }
  return names
}
