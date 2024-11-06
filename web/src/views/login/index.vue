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
        <h5 v-show="isLogin" f-c-c text-24 font-normal color="#6a6a6a">
          <icon-custom-logo mr-10 text-50 color-primary />{{ $t('app_name') }}
        </h5>
        <h5 v-show="!isLogin" f-c-c text-24 font-normal color="#6a6a6a">
          <icon-custom-logo mr-10 text-50 color-primary />{{ $t('app_name') }} - 注册
        </h5>

        <div v-show="isLogin" mt-30>
          <n-input
            v-model:value="loginInfo.username"
            autofocus
            class="h-50 items-center pl-10 text-16"
            placeholder="admin"
            :maxlength="20"
          />
        </div>
        <div v-show="!isLogin" mt-30>
          <n-input
            v-model:value="registerInfo.username"
            autofocus
            class="h-50 items-center pl-10 text-16"
            placeholder="新用户名"
            :maxlength="20"
          />
        </div>

        <div v-show="isLogin" mt-30>
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
        <div v-show="!isLogin" mt-30>
          <n-input
            v-model:value="registerInfo.email"
            class="h-50 items-center pl-10 text-16"
            type="text"
            show-password-on="mousedown"
            placeholder="邮箱"
            :maxlength="20"
          />
        </div>
        <div v-show="!isLogin" mt-30>
          <n-input
            v-model:value="registerInfo.password"
            class="h-50 items-center pl-10 text-16"
            type="password"
            show-password-on="mousedown"
            placeholder="新密码"
            :maxlength="20"
          />
        </div>

        <div v-show="!isLogin" mt-30>
          <n-input
            v-model:value="registerInfo.confirmPassword"
            class="h-50 items-center pl-10 text-16"
            type="password"
            show-password-on="mousedown"
            placeholder="确认密码"
            :maxlength="20"
          />
        </div>

        <div mt-20>
          <n-button
            v-show="isLogin"
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
          <n-button
            v-show="!isLogin"
            h-50
            w-full
            rounded-5
            text-16
            type="primary"
            :loading="loading"
            @click="handleRegister"
          >
            注册
          </n-button>
        </div>

        <!-- 添加提示文本和点击事件 -->
        <div mt-10 text-center>
          <span v-show="isLogin" class="text-white cursor-pointer" @click="isLogin = false">无账号？点击注册</span>
          <span v-show="!isLogin" class="text-white cursor-pointer" @click="isLogin = true">已有账号？点击登录</span>
        </div>
      </div>
    </div>
  </AppPage>
</template>

<script setup>
import { ref } from 'vue';
import { lStorage, setToken } from '@/utils'; // 导入本地存储和设置Token的工具函数
import bgImg from '@/assets/images/login_bg.webp'; // 导入背景图片
import api from '@/api'; // 导入API模块
import { addDynamicRoutes } from '@/router'; // 导入动态路由添加函数
import { useI18n } from 'vue-i18n'; // 导入国际化工具
import { useCRUD } from '@/composables'; // 导入CRUD组合式函数

const router = useRouter(); // 获取路由实例
const { query } = useRoute(); // 获取路由查询参数
const { t } = useI18n({ useScope: 'global' }); // 获取国际化翻译函数

// 定义登录信息响应式变量
const loginInfo = ref({
  username: '',
  password: '',
});

// 定义注册信息响应式变量
const registerInfo = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
});

// 初始化登录信息
initLoginInfo();

function initLoginInfo() {
  const localLoginInfo = lStorage.get('loginInfo'); // 从本地存储获取登录信息
  if (localLoginInfo) {
    loginInfo.value.username = localLoginInfo.username || ''; // 设置用户名
    loginInfo.value.password = localLoginInfo.password || ''; // 设置密码
  }
}

// 定义加载状态响应式变量
const loading = ref(false);

// 定义是否显示登录表单的响应式变量
const isLogin = ref(true);

// 使用CRUD组合式函数
const {
  modalVisible,
  modalTitle,
  modalAction,
  modalLoading,
  handleSave,
  modalForm,
  modalFormRef,
  handleEdit,
  handleDelete,
  handleAdd,
} = useCRUD({
  name: '用户',
  initForm: {},
  doCreate: api.createUser,
  doUpdate: api.updateUser,
  doDelete: api.deleteUser,
  refresh: () => $table.value?.handleSearch(),
});

// 处理登录逻辑的异步函数
async function handleLogin() {
  const { username, password } = loginInfo.value; // 获取用户名和密码
  if (!username || !password) {
    $message.warning(t('views.login.message_input_username_password')); // 提示输入用户名和密码
    return;
  }
  try {
    loading.value = true; // 设置加载状态为true
    $message.loading(t('views.login.message_login_success')); // 显示登录成功提示
    const res = await api.login({ username, password: password.toString() }); // 调用登录API
    $message.success(t('views.login.message_login_success')); // 显示登录成功提示
    setToken(res.data.access_token); // 设置Token
    await addDynamicRoutes(); // 添加动态路由
    if (query.redirect) {
      // 如果有重定向参数
      const path = query.redirect; // 获取重定向路径
      console.log('path', { path, query }); // 打印路径和查询参数
      Reflect.deleteProperty(query, 'redirect'); // 删除重定向参数
      router.push({ path, query }); // 跳转到重定向路径
    } else {
      router.push('/'); // 跳转到首页
    }
  } catch (e) {
    console.error('login error', e.error); // 捕获并打印登录错误
  }
  loading.value = false; // 设置加载状态为false
}

// 处理注册逻辑的异步函数
async function handleRegister() {
  const { username, email, password, confirmPassword } = registerInfo.value; // 获取注册信息
  if (!username || !email || !password || !confirmPassword) {
    $message.warning('请输入用户名、邮箱、密码和确认密码'); // 提示输入用户名、邮箱、密码和确认密码
    return;
  }
  if (password !== confirmPassword) {
    $message.warning('密码和确认密码不一致'); // 提示密码和确认密码不一致
    return;
  }
  try {
    loading.value = true; // 设置加载状态为true
    $message.loading('注册中...'); // 显示注册中提示

    // 调用 handleSave 函数来保存用户信息
    await handleSave({ username, email, password: password.toString() });

    $message.success('注册成功'); // 显示注册成功提示
    isLogin.value = true; // 切换回登录表单
  } catch (e) {
    console.error('register error', e.error); // 捕获并打印注册错误
    $message.error(e.message || '注册失败，请稍后再试'); // 显示错误信息
  } finally {
    loading.value = false; // 设置加载状态为false
  }
}
</script>