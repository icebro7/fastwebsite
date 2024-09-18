import { defineStore } from 'pinia' // 导入 Pinia 的 defineStore 函数
import { resetRouter } from '@/router' // 导入重置路由的函数
import { useTagsStore, usePermissionStore } from '@/store' // 导入标签页和权限相关的 store
import { removeToken, toLogin } from '@/utils' // 导入移除 token 和跳转到登录页的工具函数
import api from '@/api' // 导入 API 请求工具

export const useUserStore = defineStore('user', {
  state() {
    return {
      userInfo: {}, // 用户信息
    }
  },
  getters: {
    userId() {
      return this.userInfo?.id // 获取用户 ID
    },
    name() {
      return this.userInfo?.username // 获取用户名
    },
    email() {
      return this.userInfo?.email // 获取用户邮箱
    },
    avatar() {
      return this.userInfo?.avatar // 获取用户头像
    },
    role() {
      return this.userInfo?.roles || [] // 获取用户角色
    },
    isSuperUser() {
      return this.userInfo?.is_superuser // 判断是否为超级用户
    },
    isActive() {
      return this.userInfo?.is_active // 判断用户是否激活
    },
  },
  actions: {
    async getUserInfo() {
      try {
        const res = await api.getUserInfo() // 调用接口获取用户信息
        if (res.code === 401) {
          this.logout() // 如果返回 401 状态码，执行登出操作
          return
        }
        const { id, username, email, avatar, roles, is_superuser, is_active } = res.data
        this.userInfo = { id, username, email, avatar, roles, is_superuser, is_active } // 更新用户信息
        return res.data
      } catch (error) {
        return error
      }
    },
    async logout() {
      const { resetTags } = useTagsStore() // 获取标签页 store 的 resetTags 方法
      const { resetPermission } = usePermissionStore() // 获取权限 store 的 resetPermission 方法
      removeToken() // 移除 token
      resetTags() // 重置标签页
      resetPermission() // 重置权限
      resetRouter() // 重置路由
      this.$reset() // 重置 store 状态
      toLogin() // 跳转到登录页
    },
    setUserInfo(userInfo = {}) {
      this.userInfo = { ...this.userInfo, ...userInfo } // 更新用户信息
    },
  },
})
