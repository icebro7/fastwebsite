<template>
  <div v-if="reloadFlag" class="relative">
    <slot></slot>
    <div v-show="showPlaceholder" class="absolute-lt h-full w-full" :class="placeholderClass">
      <div v-show="loading" class="absolute-center">
        <n-spin :show="true" :size="loadingSize" />
      </div>
      <div v-show="isEmpty" class="absolute-center">
        <div class="relative">
          <icon-custom-no-data :class="iconClass" />
          <p class="absolute-lb w-full text-center" :class="descClass">{{ emptyDesc }}</p>
        </div>
      </div>
      <div v-show="!network" class="absolute-center">
        <div
          class="relative"
          :class="{ 'cursor-pointer': showNetworkReload }"
          @click="handleReload"
        >
          <icon-custom-network-error :class="iconClass" />
          <p class="absolute-lb w-full text-center" :class="descClass">{{ networkErrorDesc }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, watch, onUnmounted } from 'vue' // 导入 Vue 3 的相关函数

defineOptions({ name: 'LoadingEmptyWrapper' }) // 定义组件名称为 LoadingEmptyWrapper

const NETWORK_ERROR_MSG = '网络似乎开了小差~' // 定义网络错误信息

const props = {
  loading: false, // 是否正在加载
  empty: false, // 数据是否为空
  loadingSize: 'medium', // 加载图标的大小
  placeholderClass: 'bg-white dark:bg-dark transition-background-color duration-300 ease-in-out', // 占位符的样式类
  emptyDesc: '暂无数据', // 数据为空时的描述
  iconClass: 'text-320px text-primary', // 图标的样式类
  descClass: 'text-16px text-#666', // 描述的样式类
  showNetworkReload: false, // 是否显示网络重试按钮
}

// 网络状态
const network = ref(window.navigator.onLine) // 获取当前网络状态
const reloadFlag = ref(true) // 重载标志

// 数据是否为空
const isEmpty = computed(() => props.empty && !props.loading && network.value) // 计算属性，判断数据是否为空

const showPlaceholder = computed(() => props.loading || isEmpty.value || !network.value) // 计算属性，判断是否显示占位符

const networkErrorDesc = computed(
  () => (props.showNetworkReload ? `${NETWORK_ERROR_MSG}, 点击重试` : NETWORK_ERROR_MSG) // 计算属性，根据是否显示重试按钮生成网络错误描述
)

function handleReload() {
  if (!props.showNetworkReload) return // 如果不显示重试按钮，则直接返回
  reloadFlag.value = false // 设置重载标志为 false
  nextTick(() => {
    reloadFlag.value = true // 在下一次 DOM 更新后，设置重载标志为 true
  })
}

const stopHandle = watch(
  () => props.loading,
  (newValue) => {
    // 结束加载判断一下网络状态
    if (!newValue) {
      network.value = window.navigator.onLine // 如果加载结束，更新网络状态
    }
  }
)

onUnmounted(() => {
  stopHandle() // 组件卸载时停止监听
})
</script>

<style scoped></style>
