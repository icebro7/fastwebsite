<!--创建一个图标选择器，支持搜索和选择图标-->

<script setup>
import { ref } from 'vue' // 导入 Vue 的 ref 函数
import { watchDebounced } from '@vueuse/core' // 导入 @vueuse/core 的 watchDebounced 函数
import { NInput, NPopover } from 'naive-ui' // 导入 Naive UI 的 NInput 和 NPopover 组件

import TheIcon from './TheIcon.vue' // 导入 TheIcon 组件
import iconData from '@/assets/js/icons' // 导入图标数据

const props = defineProps({ value: String }) // 定义组件的 props，接收一个字符串类型的 value
const emit = defineEmits(['update:value']) // 定义组件的 emits，触发 update:value 事件

const choosed = ref(props.value) // 定义一个响应式变量 choosed，初始值为传入的 value
const icons = ref(iconData) // 定义一个响应式变量 icons，初始值为图标数据

// 过滤图标函数
function filterIcons() {
  icons.value = iconData.filter((item) => item.includes(choosed.value))
}

// 选择图标函数
function selectIcon(icon) {
  choosed.value = icon // 更新 choosed 的值
  emit('update:value', choosed.value) // 触发 update:value 事件，传递新的值
}

// 使用 watchDebounced 监听 choosed 的变化，防抖处理
watchDebounced(
  choosed,
  () => {
    filterIcons() // 过滤图标
    emit('update:value', choosed.value) // 触发 update:value 事件，传递新的值
  },
  { debounce: 200 }, // 设置防抖时间为 200 毫秒
)
</script>

<template>
  <div class="w-full">
    <NPopover trigger="click" placement="bottom-start">
      <template #trigger>
        <NInput v-model:value="choosed" placeholder="请输入图标名称" @update:value="filterIcons">
          <template #prefix>
            <span class="i-mdi:magnify text-18" />
          </template>
          <template #suffix>
            <TheIcon :icon="choosed" :size="18" />
          </template>
        </NInput>
      </template>
      <template #footer>
        更多图标去
        <a class="text-blue" target="_blank" href="https://icones.js.org/collection/all">
          Icones
        </a>
        查看
      </template>
      <ul v-if="icons.length" class="h-150 w-300 overflow-y-scroll">
        <li
          v-for="(icon, index) in icons"
          :key="index"
          class="mx-5 inline-block cursor-pointer hover:text-cyan"
          @click="selectIcon(icon)"
        >
          <TheIcon :icon="icon" :size="18" />
        </li>
      </ul>
      <div v-else>
        <TheIcon :icon="choosed" :size="18" />
      </div>
    </NPopover>
  </div>
</template>
