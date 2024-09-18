<template>
  <div>
    <h1>功能页面</h1>
    <div class="container">
      <div class="box" @mouseover="enlarge(0)" @mouseout="reset(0)" @click="openModal(0)">
        基于Flask的全国招聘系统
        <transition name="fade">
          <div v-show="enlargedIndex === 0" class="additional-info">
            功能：分析与比较全国各地、各职业、各学历之间关系，有助于求职<br />
            前端:Bootstrap、JavaScript、Echarts 、Ajax <br />
            后端：Flask、Python、Hash 、Requests<br />
            数据库：Sqlite3、SQLAlchemy<br />
            基于以上技术，实现了该全国招聘分析系统。
          </div>
        </transition>
      </div>
      <div class="box" @mouseover="enlarge(1)" @mouseout="reset(1)" @click="openModal(1)">
        标签二
        <transition name="fade">
          <div v-show="enlargedIndex === 1" class="additional-info">
            这是标签二的相关信息。
          </div>
        </transition>
      </div>
    </div>
    <div class="container">
      <div class="box" @mouseover="enlarge(2)" @mouseout="reset(2)" @click="openModal(2)">
        标签三
        <transition name="fade">
          <div v-show="enlargedIndex === 2" class="additional-info">
            这是标签三的相关信息。
          </div>
        </transition>
      </div>
      <div class="box" @mouseover="enlarge(3)" @mouseout="reset(3)" @click="openModal(3)">
        标签四
        <transition name="fade">
          <div v-show="enlargedIndex === 3" class="additional-info">
            这是标签四的相关信息。
          </div>
        </transition>
      </div>
    </div>

    <!-- 模态框 -->
    <transition name="modal">
      <div v-if="showModal" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <h2>详细信息</h2>
          <div v-if="isLoading" class="loading">视频加载中...</div>
          <video v-else ref="videoPlayer" controls width="85%" height="auto">
            <source :src="videoSrc" type="video/mp4">
            Your browser does not support the video tag.
          </video>
          <div class="button-container">
            <button class="download-button" @click="downloadFile">下载项目</button>
            <button class="download-button" @click="closeModal">关闭</button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      enlargedIndex: -1,
      showModal: false,
      modalContent: '',
      isLoading: false,
      videoSrc: '',
      modalData: [
        '这是一个基于Flask框架的全国招聘系统，支持职位发布、简历投递等功能。',
        '这是标签二的相关信息。',
        '这是标签三的相关信息。',
        '这是标签四的相关信息。',
      ],
    }
  },
  methods: {
    enlarge(index) {
      this.enlargedIndex = index
    },
    reset(index) {
      if (this.enlargedIndex === index) {
        this.enlargedIndex = -1
      }
    },
    async openModal(index) {
      this.modalContent = this.modalData[index];
      this.showModal = true;

      if (index === 0) {
        this.isLoading = true;
        await this.fetchVideo();
      }
    },
    closeModal() {
      this.showModal = false;
      this.videoSrc = '';
    },
    async fetchVideo() {
      try {
        const response = await axios.get(
            '/api/v1/video/show-video?video_name=project1.mp4',
            {
          responseType: 'blob',
        })
        const blob = new Blob([response.data], { type: 'video/mp4' });
        this.videoSrc = URL.createObjectURL(blob);
        this.isLoading = false;
      } catch (error) {
        console.error('Error fetching video:', error);
        this.isLoading = false;
      }
    },
    async downloadFile() {
      try {
        const response = await axios.get(
          '/api/v1/video/download-rar?project_name=flaskProject.rar',
          {
            responseType: 'blob',
          }
        )
        const blob = new Blob([response.data]);
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'flaskProject.rar';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      } catch (error) {
        console.error('Error downloading file:', error);
      }
    },
  },
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

.box {
  width: 400px;
  height: 250px;
  background-color: rgba(154, 153, 153, 0.48);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border 0.3s ease;
  margin: 70px; /* 增加标签之间的相对上下和左右间隔 */
  border: 2px solid transparent; /* 初始边框透明 */
  border-radius: 20px; /* 设置圆角半径 */
  position: relative; /* 确保子元素的定位是相对于父元素 */
  overflow: hidden; /* 隐藏超出部分 */
  cursor: pointer;
}

.box:hover {
  transform: scale(1.5);
  box-shadow: 0 0 20px #ffcc00; /* 增加阴影效果 */
  border: 2px solid #ffcc00; /* 增加轮廓光效果 */
}

.additional-info {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #ccc;
  color: white;
  padding: 20px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 过渡效果 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter, .fade-leave-to {
  opacity: 0;
}

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;

  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-content {
  background-color: rgba(154, 153, 153, 1);
  padding: 20px;
  border-radius: 10px;
  width: 80%;
  height: 100%;
  max-width: 80%;
  max-height: 80%;
  text-align: center;
  position: relative;
  top: 45%;
  left: 45%;
  transform: translate(-50%, -50%);
}

.modal-content h2 {
  margin-top: 0;
}

.button-container {
  position: absolute;
  bottom: 10%; /* 按钮距离底部20%的高度 */
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  justify-content: center;
}

.modal-content button {
  margin-top: 20px;
}

/* 模态框过渡效果 */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter, .modal-leave-to {
  opacity: 0;
}
.loading {
  color: white;
  font-size: 18px;
  margin-bottom: 20px;
}

.modal-content button {
  margin-top: 20px;
  margin-right: 50px; /* 添加按钮之间的间距 */
}

/* 下载按钮样式 */
.download-button {
  display: inline-block;
  padding: 20px 40px;
  background-color: rgba(255, 165, 0, 0.8);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  text-decoration: none;
  transition: box-shadow 0.3s ease, transform 0.3s ease; /* 添加过渡效果 */
  margin-right: 10px; /* 添加按钮之间的间距 */
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
</style>
