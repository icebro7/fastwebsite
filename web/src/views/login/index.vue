<template>
  <AppPage :show-footer="true" bg-cover :style="{ backgroundImage: `url(${bgImg})` }">
    <div
      style="transform: translateY(25px)"
      class="m-auto max-w-1500 min-w-345 f-c-c rounded-10 bg-white bg-opacity-60 p-15 card-shadow"
      dark:bg-dark
    >
      <div hidden w-380 px-20 py-35 md:block>
        <icon-custom-front-page pt-10 text-300 color-primary></icon-custom-front-page>
      </div>

      <div w-320 flex-col px-20 py-35>
        <h5 f-c-c text-24 font-normal color="#6a6a6a">
          <icon-custom-logo mr-10 text-50 color-primary />{{ $t('app_name') }}
        </h5>
        <div mt-30>
          <n-input
            v-model:value="loginInfo.username"
            autofocus
            class="h-50 items-center pl-10 text-16"
            placeholder="admin"
            :maxlength="20"
          />
        </div>
        <div mt-30>
          <n-input
            v-model:value="loginInfo.password"
            class="h-50 items-center pl-10 text-16"
            type="password"
            show-password-on="mousedown"
            placeholder="123456"
            :maxlength="20"
            @keypress.enter="handleLogin"
          />
        </div>

        <div mt-20>
          <n-button
            h-50
            w-full
            rounded-5
            text-16
            type="primary"
            :loading="loading"
            @click="handleLogin"
          >
            {{ $t('views.login.text_login') }}
          </n-button>
        </div>
      </div>
    </div>
  </AppPage>
</template>

<script setup>
import { lStorage, setToken } from '@/utils' // 导入本地存储和设置Token的工具函数
import bgImg from '@/assets/images/login_bg.webp' // 导入背景图片
import api from '@/api' // 导入API模块
import { addDynamicRoutes } from '@/router' // 导入动态路由添加函数
import { useI18n } from 'vue-i18n' // 导入国际化工具

const router = useRouter() // 获取路由实例
const { query } = useRoute() // 获取路由查询参数
const { t } = useI18n({ useScope: 'global' }) // 获取国际化翻译函数

// 定义登录信息响应式变量
const loginInfo = ref({
  username: '',
  password: '',
})

// 初始化登录信息
initLoginInfo()

function initLoginInfo() {
  const localLoginInfo = lStorage.get('loginInfo') // 从本地存储获取登录信息
  if (localLoginInfo) {
    loginInfo.value.username = localLoginInfo.username || '' // 设置用户名
    loginInfo.value.password = localLoginInfo.password || '' // 设置密码
  }
}

// 定义加载状态响应式变量
const loading = ref(false)

// 处理登录逻辑的异步函数
async function handleLogin() {
  const { username, password } = loginInfo.value // 获取用户名和密码
  if (!username || !password) {
    $message.warning(t('views.login.message_input_username_password')) // 提示输入用户名和密码
    return
  }
  try {
    loading.value = true // 设置加载状态为true
    $message.loading(t('views.login.message_login_success')) // 显示登录成功提示
    const res = await api.login({ username, password: password.toString() }) // 调用登录API
    $message.success(t('views.login.message_login_success')) // 显示登录成功提示
    setToken(res.data.access_token) // 设置Token
    await addDynamicRoutes() // 添加动态路由
    if (query.redirect) {
      // 如果有重定向参数
      const path = query.redirect // 获取重定向路径
      console.log('path', { path, query }) // 打印路径和查询参数
      Reflect.deleteProperty(query, 'redirect') // 删除重定向参数
      router.push({ path, query }) // 跳转到重定向路径
    } else {
      router.push('/') // 跳转到首页
    }
  } catch (e) {
    console.error('login error', e.error) // 捕获并打印登录错误
  }
  loading.value = false // 设置加载状态为false
}
</script>
