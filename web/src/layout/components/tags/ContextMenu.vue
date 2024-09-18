<!--标签页操作的下拉菜单-->
<template>
  <n-dropdown
    :show="show"
    :options="options"
    :x="x"
    :y="y"
    placement="bottom-start"
    @clickoutside="handleHideDropdown"
    @select="handleSelect"
  />
</template>

<script setup>
import { useTagsStore, useAppStore } from '@/store' // 导入标签页和应用状态管理
import { renderIcon } from '@/utils' // 导入图标渲染工具

// 定义组件的属性，包括 show、currentPath、x、y
const props = defineProps({
  show: {
    type: Boolean,
    default: false,
  },
  currentPath: {
    type: String,
    default: '',
  },
  x: {
    type: Number,
    default: 0,
  },
  y: {
    type: Number,
    default: 0,
  },
})

// 定义组件的事件发射器
const emit = defineEmits(['update:show'])

const tagsStore = useTagsStore()
const appStore = useAppStore()

// 计算属性，生成下拉菜单的选项
const options = computed(() => [
  {
    label: '重新加载',
    key: 'reload',
    disabled: props.currentPath !== tagsStore.activeTag,
    icon: renderIcon('mdi:refresh', { size: '14px' }),
  },
  {
    label: '关闭',
    key: 'close',
    disabled: tagsStore.tags.length <= 1,
    icon: renderIcon('mdi:close', { size: '14px' }),
  },
  {
    label: '关闭其他',
    key: 'close-other',
    disabled: tagsStore.tags.length <= 1,
    icon: renderIcon('mdi:arrow-expand-horizontal', { size: '14px' }),
  },
  {
    label: '关闭左侧',
    key: 'close-left',
    disabled: tagsStore.tags.length <= 1 || props.currentPath === tagsStore.tags[0].path,
    icon: renderIcon('mdi:arrow-expand-left', { size: '14px' }),
  },
  {
    label: '关闭右侧',
    key: 'close-right',
    disabled:
      tagsStore.tags.length <= 1 ||
      props.currentPath === tagsStore.tags[tagsStore.tags.length - 1].path,
    icon: renderIcon('mdi:arrow-expand-right', { size: '14px' }),
  },
])

const route = useRoute()
// 操作映射表，定义每个菜单项对应的操作函数
const actionMap = new Map([
  [
    'reload',
    () => {
      if (route.meta?.keepAlive) {
        // 重置keepAlive
        appStore.setAliveKeys(route.name, +new Date())
      }
      appStore.reloadPage()
    },
  ],
  [
    'close',
    () => {
      tagsStore.removeTag(props.currentPath)
    },
  ],
  [
    'close-other',
    () => {
      tagsStore.removeOther(props.currentPath)
    },
  ],
  [
    'close-left',
    () => {
      tagsStore.removeLeft(props.currentPath)
    },
  ],
  [
    'close-right',
    () => {
      tagsStore.removeRight(props.currentPath)
    },
  ],
])

// 隐藏下拉菜单的函数
function handleHideDropdown() {
  emit('update:show', false)
}

// 处理菜单项选择事件的函数
function handleSelect(key) {
  const actionFn = actionMap.get(key)
  actionFn && actionFn()
  handleHideDropdown()
}
</script>
