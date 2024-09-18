<template>
  <section :class="['background-section', { 'dark-theme': isDark }]">
    <div class="container">
      <div class="input-container">
        <input v-model="url" type="text" placeholder="请输入网址" class="input-field" @keyup.enter="crawlUrl" />
        <button @click="crawlUrl" class="button">爬取样式并下载</button>
      </div>
      <div v-if="isLoading" class="loading-spinner">
        <div class="spinner"></div>
      </div>
      <div v-if="downloadLink && !isLoading" class="download-link">
        <a :href="downloadLink" download class="download-button">点击下载样式文件</a>
      </div>
    </div>
  </section>
</template>

<script>
import axios from 'axios'
import { useAppStore } from '@/store' // 导入应用状态管理
import { useDark } from '@vueuse/core' // 导入暗色主题

export default {
  data() {
    return {
      url: '', // 用于存储用户输入的网址
      downloadLink: '', // 用于存储生成的下载链接
      isLoading: false, // 用于控制加载动画的显示
    }
  },
  computed: {
    isDark() {
      return useAppStore().isDark // 获取当前主题
    },
  },
  methods: {
    async crawlUrl() {
      // 清除之前的下载链接
      this.downloadLink = ''
      // 显示加载动画
      this.isLoading = true

      try {
        const response = await axios.post('/api/v1/copy/crawl-url', { url: this.url })
        if (response.data && response.data.download_link) {
          this.downloadLink = `/api/v1/copy/download/${response.data.download_link
            .split('/')
            .pop()}`
        } else {
          console.error('No download link returned from the server')
        }
      } catch (error) {
        console.error('爬取样式失败:', error)
      } finally {
        // 3秒后隐藏加载动画
        setTimeout(() => {
          this.isLoading = false
        }, 3000)
      }
    },
  },
}
</script>

<style scoped>
/* 设置背景图片 */
.background-section {
  position: relative; /* 设置相对定位 */
  height: 100vh; /* 使容器占满整个视口高度 */
  background-size: cover; /* 背景图片覆盖整个容器 */
  background-position: center; /* 背景图片居中 */
  background-repeat: no-repeat; /* 背景图片不重复 */
}

/* 普通主题背景图片 */
.background-section:not(.dark-theme) {
  background-image: url('../../assets/images/background2.webp'); /* 设置背景图片 */
}

/* 暗色主题背景图片 */
.background-section.dark-theme {
  background-image: url('../../assets/images/background1.webp'); /* 设置背景图片 */
}

/* 使用 flexbox 布局将内容垂直居中 */
.container {
  position: absolute; /* 设置绝对定位 */
  top: 3vh; /* 使容器位于从上至下的六分之一处 */
  left: 50%; /* 水平居中 */
  transform: translateX(-50%); /* 水平居中 */
  display: flex;
  justify-content: center;
  align-items: center;
  height: 33.33vh; /* 使容器占满整个视口高度的六分之二 */
  flex-direction: column; /* 垂直排列子元素 */
}

/* 输入框和按钮的容器 */
.input-container {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px; /* 与下载链接的间距 */
}

/* 输入框样式 */
.input-field {
  width: 500px;
  padding: 25px;
  margin-right: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* 添加过渡效果 */
}

/* 鼠标悬停时输入框的样式 */
.input-field:hover {
  box-shadow: 0 0 20px rgba(255, 165, 0, 0.8); /* 增加阴影范围和模糊度 */
}

/* 输入框获得焦点时的样式 */
.input-field:focus {
  transform: translateY(-5px); /* 向上移动 */
  box-shadow: 0 5px 20px rgba(255, 165, 0, 0.8); /* 增加阴影范围和模糊度 */
}

/* 按钮样式 */
.button {
  padding: 25px 40px;
  background-color: rgba(154, 153, 153, 0.48);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* 添加过渡效果 */
}

/* 鼠标悬停时按钮的样式 */
.button:hover {
  background-color: rgba(255, 165, 0, 0.8);
  transform: translateY(-5px); /* 向上移动 */
  box-shadow: 0 5px 20px rgba(255, 165, 0, 0.8); /* 增加阴影范围和模糊度 */
}

/* 按钮获得焦点时的样式 */
.button:focus {
  transform: translateY(-5px); /* 向上移动 */
  box-shadow: 0 5px 20px rgba(255, 165, 0, 0.8); /* 增加阴影范围和模糊度 */
}

/* 下载链接样式 */
.download-link {
  text-align: center;
}

/* 下载按钮样式 */
.download-button {
  display: inline-block;
  padding: 15px 30px;
  background-color: rgba(154, 153, 153, 0.48);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* 添加过渡效果 */
}

/* 鼠标悬停时下载按钮的样式 */
.download-button:hover {
  background-color: #42b983;
  transform: translateY(-5px); /* 向上移动 */
  box-shadow: 0 5px 20px #42b983; /* 增加阴影范围和模糊度 */
}

/* 下载按钮获得焦点时的样式 */
.download-button:focus {
  transform: translateY(-5px); /* 向上移动 */
  box-shadow: 0 5px 20px rgba(255, 165, 0, 0.8); /* 增加阴影范围和模糊度 */
}

/* 加载动画样式 */
.loading-spinner {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border-top-color: #42b983;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>