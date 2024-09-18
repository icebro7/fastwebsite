import { useUserStore, usePermissionStore } from '@/store'

// 检查用户是否具有指定的权限
function hasPermission(permission) {
  const userStore = useUserStore()
  const userPermissionStore = usePermissionStore()
  // 获取用户权限列表
  const accessApis = userPermissionStore.apis
  if (userStore.isSuperUser) {
    return true
  }
  return accessApis.includes(permission)
}

// 安装自定义的vue指令
export default function setupPermissionDirective(app) {
  // 更新元素的可见性
  function updateElVisible(el, permission) {
    if (!permission) {
      throw new Error(`need roles: like v-permission="get/api/v1/user/list"`)
    }
    if (!hasPermission(permission)) {
      el.parentElement?.removeChild(el)
    }
  }
  //定义了指令的生命周期钩子函数
  const permissionDirective = {
    mounted(el, binding) {
      updateElVisible(el, binding.value)
    },
    beforeUpdate(el, binding) {
      updateElVisible(el, binding.value)
    },
  }

  app.directive('permission', permissionDirective)
}
