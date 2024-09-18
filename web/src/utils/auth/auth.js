import { router } from '@/router' // 导入路由实例

// 跳转到登录页
export function toLogin() {
  const currentRoute = unref(router.currentRoute) // 获取当前路由信息
  const needRedirect =
    !currentRoute.meta.requireAuth && !['/404', '/login'].includes(router.currentRoute.value.path) // 判断是否需要重定向
  router.replace({
    path: '/login', // 跳转到登录页
    query: needRedirect ? { ...currentRoute.query, redirect: currentRoute.path } : {}, // 如果需要重定向，则添加重定向参数
  })
}

// 跳转到 404 页面
export function toFourZeroFour() {
  router.replace({
    path: '/404', // 跳转到 404 页面
  })
}
