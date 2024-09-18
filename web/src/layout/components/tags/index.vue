<!--标签页导航栏-->
<template>
  <ScrollX ref="scrollXRef" class="bg-white dark:bg-dark!">
    <n-tag
      v-for="tag in tagsStore.tags"
      ref="tabRefs"
      :key="tag.path"
      class="mx-5 cursor-pointer rounded-4 px-15 hover:color-primary"
      :type="tagsStore.activeTag === tag.path ? 'primary' : 'default'"
      :closable="tagsStore.tags.length > 1"
      @click="handleTagClick(tag.path)"
      @close.stop="tagsStore.removeTag(tag.path)"
      @contextmenu.prevent="handleContextMenu($event, tag)"
    >
      {{ tag.title }}
    </n-tag>
    <ContextMenu
      v-if="contextMenuOption.show"
      v-model:show="contextMenuOption.show"
      :current-path="contextMenuOption.currentPath"
      :x="contextMenuOption.x"
      :y="contextMenuOption.y"
    />
  </ScrollX>
</template>

<script setup>
import ContextMenu from './ContextMenu.vue' // 导入右键菜单组件
import { useTagsStore } from '@/store' // 导入标签页状态管理
import ScrollX from '@/components/common/ScrollX.vue' // 导入水平滚动组件

const route = useRoute() // 获取当前路由信息
const router = useRouter() // 获取路由实例
const tagsStore = useTagsStore() // 获取标签页状态
const tabRefs = ref([]) // 标签页组件的引用
const scrollXRef = ref(null) // 水平滚动组件的引用

const contextMenuOption = reactive({
  show: false,
  x: 0,
  y: 0,
  currentPath: '',
})

watch(
  () => route.path,
  () => {
    const { name, fullPath: path } = route
    const title = route.meta?.title
    tagsStore.addTag({ name, path, title })
  },
  { immediate: true },
)

watch(
  () => tagsStore.activeIndex,
  async (activeIndex) => {
    await nextTick()
    const activeTabElement = tabRefs.value[activeIndex]?.$el
    if (!activeTabElement) return
    const { offsetLeft: x, offsetWidth: width } = activeTabElement
    scrollXRef.value?.handleScroll(x + width, width)
  },
  { immediate: true }
)

const handleTagClick = (path) => {
  tagsStore.setActiveTag(path)
  router.push(path)
}

// 控制右键菜单的显示和位置
function showContextMenu() {
  contextMenuOption.show = true
}
function hideContextMenu() {
  contextMenuOption.show = false
}
function setContextMenu(x, y, currentPath) {
  Object.assign(contextMenuOption, { x, y, currentPath })
}

// 右击菜单
async function handleContextMenu(e, tagItem) {
  const { clientX, clientY } = e
  hideContextMenu()
  setContextMenu(clientX, clientY, tagItem.path)
  await nextTick()
  showContextMenu()
}
</script>
