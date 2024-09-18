<template>
  <!-- 查询栏，如果有 queryBar 插槽则显示 -->
  <QueryBar v-if="$slots.queryBar" mb-30 @search="handleSearch" @reset="handleReset">
    <slot name="queryBar" />
  </QueryBar>

  <n-data-table
    :remote="remote"
    :loading="loading"
    :columns="columns"
    :data="tableData"
    :scroll-x="scrollX"
    :row-key="(row) => row[rowKey]"
    :pagination="isPagination ? pagination : false"
    @update:checked-row-keys="onChecked"
    @update:page="onPageChange"
  />
</template>

<script setup>
const props = defineProps({
  /**
   * @remote true: 后端分页  false： 前端分页
   */
  remote: {
    type: Boolean,
    default: true,
  },
  /**
   * @remote 是否分页
   */
  isPagination: {
    type: Boolean,
    default: true,
  },
  scrollX: {
    type: Number,
    default: 450,
  },
  rowKey: {
    type: String,
    default: 'id',
  },
  columns: {
    type: Array,
    required: true,
  },
  /** queryBar中的参数 */
  queryItems: {
    type: Object,
    default() {
      return {}
    },
  },
  /** 补充参数（可选） */
  extraParams: {
    type: Object,
    default() {
      return {}
    },
  },
  /**
   * ! 约定接口入参出参
   * * 分页模式需约定分页接口入参
   *    @page_size 分页参数：一页展示多少条，默认10
   *    @page   分页参数：页码，默认1
   */
  getData: {
    type: Function,
    required: true,
  },
})

const emit = defineEmits(['update:queryItems', 'onChecked', 'onDataChange'])
const loading = ref(false) // 加载状态
const initQuery = { ...props.queryItems } // 初始查询参数
const tableData = ref([]) // 表格数据
const pagination = reactive({
  page: 1, // 当前页码
  page_size: 10, // 每页显示条数
  pageSizes: [10, 20, 50, 100], // 可选的每页显示条数
  showSizePicker: true, // 是否显示每页显示条数选择器
  prefix({ itemCount }) {
    return `共 ${itemCount} 条` // 分页前缀显示
  },
  onChange: (page) => {
    pagination.page = page // 页码变化处理
  },
  onUpdatePageSize: (pageSize) => {
    pagination.page_size = pageSize // 每页显示条数变化处理
    pagination.page = 1 // 重置页码
    handleQuery() // 重新查询数据
  },
})

async function handleQuery() {
  try {
    loading.value = true // 设置加载状态
    let paginationParams = {}
    // 如果非分页模式或者使用前端分页,则无需传分页参数
    if (props.isPagination && props.remote) {
      paginationParams = { page: pagination.page, page_size: pagination.page_size }
    }
    const { data, total } = await props.getData({
      ...props.queryItems,
      ...props.extraParams,
      ...paginationParams,
    })
    tableData.value = data // 更新表格数据
    pagination.itemCount = total || 0 // 更新总条数
  } catch (error) {
    tableData.value = [] // 清空表格数据
    pagination.itemCount = 0 // 清空总条数
  } finally {
    emit('onDataChange', tableData.value) // 触发数据变化事件
    loading.value = false // 取消加载状态
  }
}

function handleSearch() {
  pagination.page = 1 // 重置页码
  handleQuery() // 重新查询数据
}

async function handleReset() {
  const queryItems = { ...props.queryItems }
  for (const key in queryItems) {
    queryItems[key] = '' // 清空查询参数
  }
  emit('update:queryItems', { ...queryItems, ...initQuery }) // 更新查询参数
  await nextTick()
  pagination.page = 1 // 重置页码
  handleQuery() // 重新查询数据
}

function onPageChange(currentPage) {
  pagination.page = currentPage // 更新当前页码
  if (props.remote) {
    handleQuery() // 如果是后端分页，重新查询数据
  }
}

function onChecked(rowKeys) {
  if (props.columns.some((item) => item.type === 'selection')) {
    emit('onChecked', rowKeys) // 触发选中行事件
  }
}

defineExpose({
  handleSearch, // 暴露搜索方法
  handleReset, // 暴露重置方法
  tableData, // 暴露表格数据
})
</script>
