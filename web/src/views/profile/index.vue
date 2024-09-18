<script setup>
import { ref } from 'vue' // 导入Vue的ref函数
import { NButton, NForm, NFormItem, NInput, NTabPane, NTabs, NImage } from 'naive-ui' // 导入Naive UI组件
import { useI18n } from 'vue-i18n' // 导入国际化工具
import CommonPage from '@/components/page/CommonPage.vue' // 导入通用页面组件
import { useUserStore } from '@/store' // 导入用户状态管理
import api from '@/api' // 导入API模块
import { is } from '~/src/utils' // 导入工具函数

const { t } = useI18n() // 获取国际化翻译函数
const userStore = useUserStore() // 获取用户状态管理实例
const isLoading = ref(false) // 定义加载状态响应式变量

// 用户信息的表单
const infoFormRef = ref(null) // 用户信息表单引用
const infoForm = ref({
  avatar: userStore.avatar, // 用户头像
  username: userStore.name, // 用户名
  email: userStore.email, // 用户邮箱
})

// 更新用户信息的异步函数
async function updateProfile() {
  isLoading.value = true // 设置加载状态为true
  infoFormRef.value?.validate(async (err) => {
    if (err) return // 如果有错误，返回
    await api
      .updateUser({ ...infoForm.value, id: userStore.userId }) // 调用更新用户API
      .then(() => {
        userStore.setUserInfo(infoForm.value) // 更新用户信息
        isLoading.value = false // 设置加载状态为false
        $message.success(t('common.text.update_success')) // 显示更新成功提示
      })
      .catch(() => {
        isLoading.value = false // 设置加载状态为false
      })
  })
}

// 用户信息表单的验证规则
const infoFormRules = {
  username: [
    {
      required: true, // 必填项
      message: t('views.profile.message_username_required'), // 错误提示信息
      trigger: ['input', 'blur', 'change'], // 触发验证的事件
    },
  ],
}

// 修改密码的表单
const passwordFormRef = ref(null) // 修改密码表单引用
const passwordForm = ref({
  old_password: '', // 旧密码
  new_password: '', // 新密码
  confirm_password: '', // 确认新密码
})

// 更新密码的异步函数
async function updatePassword() {
  isLoading.value = true // 设置加载状态为true
  passwordFormRef.value?.validate(async (err) => {
    if (!err) {
      const data = { ...passwordForm.value, id: userStore.userId } // 准备数据
      await api
        .updatePassword(data) // 调用更新密码API
        .then((res) => {
          $message.success(res.msg) // 显示更新成功提示
          passwordForm.value = {
            old_password: '',
            new_password: '',
            confirm_password: '',
          }
          isLoading.value = false // 设置加载状态为false
        })
        .catch(() => {
          isLoading.value = false // 设置加载状态为false
        })
    }
  })
}

// 修改密码表单的验证规则
const passwordFormRules = {
  old_password: [
    {
      required: true, // 必填项
      message: t('views.profile.message_old_password_required'), // 错误提示信息
      trigger: ['input', 'blur', 'change'], // 触发验证的事件
    },
  ],
  new_password: [
    {
      required: true, // 必填项
      message: t('views.profile.message_new_password_required'), // 错误提示信息
      trigger: ['input', 'blur', 'change'], // 触发验证的事件
    },
  ],
  confirm_password: [
    {
      required: true, // 必填项
      message: t('views.profile.message_password_confirmation_required'), // 错误提示信息
      trigger: ['input', 'blur'], // 触发验证的事件
    },
    {
      validator: validatePasswordStartWith, // 自定义验证函数
      message: t('views.profile.message_password_confirmation_diff'), // 错误提示信息
      trigger: 'input', // 触发验证的事件
    },
    {
      validator: validatePasswordSame, // 自定义验证函数
      message: t('views.profile.message_password_confirmation_diff'), // 错误提示信息
      trigger: ['blur', 'password-input'], // 触发验证的事件
    },
  ],
}

// 验证新密码是否以确认密码开头
function validatePasswordStartWith(rule, value) {
  return (
    !!passwordForm.value.new_password &&
    passwordForm.value.new_password.startsWith(value) &&
    passwordForm.value.new_password.length >= value.length
  )
}

// 验证新密码和确认密码是否相同
function validatePasswordSame(rule, value) {
  return value === passwordForm.value.new_password
}
</script>

<template>
  <CommonPage :show-header="false">
    <NTabs type="line" animated>
      <NTabPane name="website" :tab="$t('views.profile.label_modify_information')">
        <div class="m-30 flex items-center">
          <NForm
            ref="infoFormRef"
            label-placement="left"
            label-align="left"
            label-width="100"
            :model="infoForm"
            :rules="infoFormRules"
            class="w-400"
          >
            <NFormItem :label="$t('views.profile.label_avatar')" path="avatar">
              <NImage width="100" :src="infoForm.avatar"></NImage>
            </NFormItem>
            <NFormItem :label="$t('views.profile.label_username')" path="username">
              <NInput
                v-model:value="infoForm.username"
                type="text"
                :placeholder="$t('views.profile.placeholder_username')"
              />
            </NFormItem>
            <NFormItem :label="$t('views.profile.label_email')" path="email">
              <NInput
                v-model:value="infoForm.email"
                type="text"
                :placeholder="$t('views.profile.placeholder_email')"
              />
            </NFormItem>
            <NButton type="primary" :loading="isLoading" @click="updateProfile">
              {{ $t('common.buttons.update') }}
            </NButton>
          </NForm>
        </div>
      </NTabPane>
      <NTabPane name="contact" :tab="$t('views.profile.label_change_password')">
        <NForm
          ref="passwordFormRef"
          label-placement="left"
          label-align="left"
          :model="passwordForm"
          label-width="200"
          :rules="passwordFormRules"
          class="m-30 w-500"
        >
          <NFormItem :label="$t('views.profile.label_old_password')" path="old_password">
            <NInput
              v-model:value="passwordForm.old_password"
              type="password"
              show-password-on="mousedown"
              :placeholder="$t('views.profile.placeholder_old_password')"
            />
          </NFormItem>
          <NFormItem :label="$t('views.profile.label_new_password')" path="new_password">
            <NInput
              v-model:value="passwordForm.new_password"
              :disabled="!passwordForm.old_password"
              type="password"
              show-password-on="mousedown"
              :placeholder="$t('views.profile.placeholder_new_password')"
            />
          </NFormItem>
          <NFormItem :label="$t('views.profile.label_confirm_password')" path="confirm_password">
            <NInput
              v-model:value="passwordForm.confirm_password"
              :disabled="!passwordForm.new_password"
              type="password"
              show-password-on="mousedown"
              :placeholder="$t('views.profile.placeholder_confirm_password')"
            />
          </NFormItem>
          <NButton type="primary" :loading="isLoading" @click="updatePassword">
            {{ $t('common.buttons.update') }}
          </NButton>
        </NForm>
      </NTabPane>
    </NTabs>
  </CommonPage>
</template>
