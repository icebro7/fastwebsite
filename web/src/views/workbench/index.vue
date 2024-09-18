<template>
  <AppPage :show-footer="false">
    <div flex-1>
      <n-card rounded-10>
        <div flex items-center justify-between>
          <div flex items-center>
            <img rounded-full width="60" :src="userStore.avatar" />
            <div ml-10>
              <p text-20 font-semibold>
                {{ $t('views.workbench.text_hello', { username: userStore.name }) }}
              </p>
              <p mt-5 text-14 op-60>{{ $t('views.workbench.text_welcome') }}</p>
            </div>
          </div>
          <n-space :size="12" :wrap="false">
            <n-statistic v-for="item in statisticData" :key="item.id" v-bind="item"></n-statistic>
          </n-space>
        </div>
      </n-card>

      <n-card
        :title="$t('views.workbench.label_project')"
        size="small"
        :segmented="true"
        mt-15
        rounded-10
      >
        <template #header-extra>
          <n-button text type="primary">{{ $t('views.workbench.label_more') }}</n-button>
        </template>
        <div flex flex-wrap justify-start>
          <n-card
            class="mb-10 mt-10 w-300 cursor-pointer"
            hover:card-shadow
            title="Fastwebsite"
            size="large"
            @click="goToTargetPage1"
          >
            <p op-60>{{ dummyText1 }}</p>
          </n-card>
          <n-card
            class="mb-10 mt-10 w-300 cursor-pointer"
            hover:card-shadow
            title="Fastwebsite"
            size="large"
            @click="goToTargetPage2"
          >
            <p op-60>{{ dummyText2 }}</p>
          </n-card>
        </div>
      </n-card>
    </div>
  </AppPage>
</template>

<script setup>
import { useUserStore } from '@/store'
import { useI18n } from 'vue-i18n'
import { router } from '@/router'

const dummyText1 = '样式获取'
const dummyText2 = '平台搭建'
const { t } = useI18n({ useScope: 'global' })

const statisticData = computed(() => [
  {
    id: 0,
    label: t('views.workbench.label_number_of_items'),
    value: '2',
  },
  {
    id: 1,
    label: t('views.workbench.label_upcoming'),
    value: '4/16',
  },
  {
    id: 2,
    label: t('views.workbench.label_information'),
    value: '12',
  },
])

const userStore = useUserStore()

const goToTargetPage1 = () => {
  router.push('/copy-site')
}
const goToTargetPage2 = () => {
  router.push('/top-menu')
}
</script>
